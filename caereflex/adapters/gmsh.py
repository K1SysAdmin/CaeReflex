from __future__ import annotations
from pathlib import Path
import re
from caereflex.core.config import CaeReflexConfig
from caereflex.core.fingerprint import sha256_file, stable_case_id
from caereflex.core.models import (
    AdapterResult, AdapterStatus, ReflexCase, CaseType, InspectionStatus, TraceInfo,
    SourceKind, SourceFileRecord, HashStatus, EngineeringAsset, AssetType,
    BoundaryConditionRecord, InspectionFlag, Severity, ProvenanceRecord
)
from caereflex.core.provenance import utc_now_iso
from caereflex.core.validation import safe_display_path
from .base import BaseAdapter

class GmshAdapter(BaseAdapter):
    name = "gmsh_adapter"

    def inspect(self, path: str | Path) -> AdapterResult:
        p = Path(path)
        workspace = p.parent if p.is_file() else p
        rel = safe_display_path(p, workspace.parent if p.is_file() else workspace)
        case_id = stable_case_id(str(p.resolve()) if p.exists() else str(p))
        case = ReflexCase(
            case_id=case_id,
            case_name=p.stem if p.is_file() else p.name,
            case_type=CaseType.gmsh,
            detected_formats=[],
            detected_tools=["Gmsh"],
            physics_tags=["mesh", "geometry"],
        )
        case.workspace.root_display = safe_display_path(workspace)
        case.provenance.append(ProvenanceRecord(event="gmsh_inspection_started", details={"path": rel}))
        warnings = []
        if not p.exists():
            case.inspection.status = InspectionStatus.failed
            msg = f"Path not found: {p}"
            case.inspection_flags.append(InspectionFlag(severity=Severity.error, category="path_not_found", message=msg))
            return AdapterResult(adapter_name=self.name, status=AdapterStatus.failed, case=case, errors=[msg])

        files = [p] if p.is_file() else [x for x in p.rglob("*") if x.is_file() and x.suffix.lower() in {'.geo','.msh','.step','.stp','.iges','.igs'}]
        for i, f in enumerate(files[: self.config.max_scan_files]):
            sha, hstatus = sha256_file(f, self.config.max_file_size_bytes)
            source = SourceFileRecord(
                file_id=f"file_{i+1}", relative_path=safe_display_path(f, workspace), suffix=f.suffix.lower(),
                size_bytes=f.stat().st_size if f.exists() else None, sha256=sha, hash_status=HashStatus(hstatus),
                trace=TraceInfo(source_kind=SourceKind.extracted, source_files=[safe_display_path(f, workspace)], adapter=self.name),
            )
            case.source_files.append(source)
            if f.suffix.lower() == '.geo':
                case.detected_formats.append('.geo')
                self._inspect_geo(f, case, workspace)
            elif f.suffix.lower() == '.msh':
                case.detected_formats.append('.msh')
                case.assets.append(EngineeringAsset(asset_id=f"asset_{len(case.assets)+1}", asset_type=AssetType.mesh, name=f.name, trace=source.trace))
                try:
                    import meshio  # type: ignore
                    mesh = meshio.read(str(f))
                    case.assets[-1].metrics.update({"points": len(mesh.points), "cell_blocks": len(mesh.cells)})
                except Exception as e:
                    warnings.append(".msh file fingerprinted; install [mesh] for deeper mesh inspection.")
                    case.inspection_flags.append(InspectionFlag(severity=Severity.warning, category="dependency_missing", message="Install [mesh] for deeper .msh inspection.", trace=source.trace))
            else:
                case.assets.append(EngineeringAsset(asset_id=f"asset_{len(case.assets)+1}", asset_type=AssetType.geometry, name=f.name, properties={"best_effort_only": True}, trace=source.trace))
                case.inspection_flags.append(InspectionFlag(severity=Severity.info, category="best_effort_geometry", message=f"{f.suffix} geometry was fingerprinted only.", trace=source.trace))

        if not case.source_files:
            case.inspection.status = InspectionStatus.failed
            msg = "No Gmsh-oriented artefacts detected."
            case.inspection_flags.append(InspectionFlag(severity=Severity.error, category="unsupported_format", message=msg))
            return AdapterResult(adapter_name=self.name, status=AdapterStatus.unsupported, case=case, errors=[msg])
        case.detected_formats = sorted(set(case.detected_formats))
        case.inspection.status = InspectionStatus.partial_success if warnings or case.inspection_flags else InspectionStatus.success
        case.inspection.completed_at = utc_now_iso()
        case.agent_summary.summary = f"Gmsh-oriented case inspected with {len(case.source_files)} source file(s)."
        case.agent_summary.do_not_claim = ["Do not claim mesh adequacy.", "Do not claim design safety."]
        return AdapterResult(adapter_name=self.name, status=AdapterStatus(case.inspection.status.value), case=case, warnings=warnings)

    def _inspect_geo(self, f: Path, case: ReflexCase, workspace: Path) -> None:
        text = f.read_text(encoding='utf-8', errors='ignore')
        rel = safe_display_path(f, workspace)
        trace = TraceInfo(source_kind=SourceKind.extracted, source_files=[rel], adapter=self.name)
        points = len(re.findall(r"\bPoint\s*\(", text))
        lines = len(re.findall(r"\bLine\s*\(", text))
        surfaces = len(re.findall(r"\b(Plane Surface|Surface)\s*\(", text))
        physicals = re.findall(r"Physical\s+(\w+)\s*\(([^)]*)\)\s*=\s*\{([^}]*)\}", text)
        case.assets.append(EngineeringAsset(
            asset_id=f"asset_{len(case.assets)+1}", asset_type=AssetType.geometry, name=f.name,
            metrics={"points_declared": points, "lines_declared": lines, "surfaces_declared": surfaces, "physical_groups": len(physicals)},
            trace=trace,
        ))
        for kind, label, members in physicals:
            case.boundary_conditions.append(BoundaryConditionRecord(
                patch=label.strip().strip('"') or f"Physical {kind}",
                field=None,
                type=f"Physical {kind}",
                value=members.strip(),
                trace=trace,
            ))
