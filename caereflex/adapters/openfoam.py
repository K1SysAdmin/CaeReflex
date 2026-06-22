from __future__ import annotations
from pathlib import Path
import re
from caereflex.core.config import CaeReflexConfig
from caereflex.core.fingerprint import sha256_file, stable_case_id
from caereflex.core.models import (
    AdapterResult, AdapterStatus, ReflexCase, CaseType, InspectionStatus, TraceInfo,
    SourceKind, SourceFileRecord, HashStatus, EngineeringAsset, AssetType,
    SolverRecord, BoundaryConditionRecord, MaterialPropertyRecord, NumericalSettingsRecord,
    ResultFieldRecord, FieldAssociation, FieldType, InspectionFlag, Severity, ProvenanceRecord
)
from caereflex.core.provenance import utc_now_iso
from caereflex.core.validation import safe_display_path
from .base import BaseAdapter

class OpenFOAMAdapter(BaseAdapter):
    name = "openfoam_adapter"
    expected = [
        'system/controlDict', 'system/fvSchemes', 'system/fvSolution',
        'constant/transportProperties', 'constant/turbulenceProperties',
        'constant/polyMesh/boundary'
    ]

    def inspect(self, path: str | Path) -> AdapterResult:
        root = Path(path)
        case_id = stable_case_id(str(root.resolve()) if root.exists() else str(root))
        case = ReflexCase(case_id=case_id, case_name=root.name, case_type=CaseType.openfoam,
                          detected_formats=['OpenFOAM case folder'], detected_tools=['OpenFOAM'],
                          physics_tags=['CFD', 'finite volume'])
        case.workspace.root_display = safe_display_path(root)
        case.provenance.append(ProvenanceRecord(event="openfoam_inspection_started", details={"path": safe_display_path(root)}))
        if not root.exists() or not root.is_dir():
            msg = "OpenFOAM path not found or not a directory."
            case.inspection.status = InspectionStatus.failed
            case.inspection_flags.append(InspectionFlag(severity=Severity.error, category="path_not_found", message=msg))
            return AdapterResult(adapter_name=self.name, status=AdapterStatus.failed, case=case, errors=[msg])

        files = []
        for rel in self.expected:
            f = root / rel
            if f.exists(): files.append(f)
            else:
                case.inspection_flags.append(InspectionFlag(severity=Severity.warning, category="missing_expected_file", message=f"Missing expected OpenFOAM file: {rel}"))
        zero_dir = root / '0'
        if zero_dir.exists():
            files.extend([f for f in zero_dir.iterdir() if f.is_file()])
        for logs in [root / 'log', root / 'log.simpleFoam', root / 'postProcessing']:
            if logs.exists():
                if logs.is_file(): files.append(logs)
                else: files.extend([f for f in logs.rglob('*') if f.is_file()][:20])

        for i, f in enumerate(dict.fromkeys(files)):
            sha, hstatus = sha256_file(f, self.config.max_file_size_bytes)
            rel = safe_display_path(f, root)
            trace = TraceInfo(source_kind=SourceKind.extracted, source_files=[rel], adapter=self.name)
            case.source_files.append(SourceFileRecord(file_id=f"file_{i+1}", relative_path=rel, suffix=f.suffix or None, size_bytes=f.stat().st_size, sha256=sha, hash_status=HashStatus(hstatus), trace=trace))
            self._parse_file(root, f, case, trace)

        case.assets.append(EngineeringAsset(asset_id="asset_openfoam_case", asset_type=AssetType.case_folder, name=root.name, metrics={"source_files": len(case.source_files)}, trace=TraceInfo(source_kind=SourceKind.extracted, source_files=[safe_display_path(root)], adapter=self.name)))
        if not case.source_files:
            msg = "No OpenFOAM case files detected."
            case.inspection.status = InspectionStatus.failed
            case.inspection_flags.append(InspectionFlag(severity=Severity.error, category="unsupported_format", message=msg))
            return AdapterResult(adapter_name=self.name, status=AdapterStatus.unsupported, case=case, errors=[msg])
        case.inspection.status = InspectionStatus.partial_success if case.inspection_flags else InspectionStatus.success
        case.inspection.completed_at = utc_now_iso()
        case.agent_summary.summary = f"OpenFOAM case inspected. {len(case.source_files)} files were considered."
        case.agent_summary.do_not_claim = ["Do not claim convergence.", "Do not claim mesh adequacy.", "Do not claim validation or certification."]
        return AdapterResult(adapter_name=self.name, status=AdapterStatus(case.inspection.status.value), case=case)

    def _parse_dict_entries(self, text: str) -> dict[str, str]:
        entries = {}
        for m in re.finditer(r"^\s*([A-Za-z0-9_]+)\s+([^;{}]+);", text, flags=re.MULTILINE):
            entries[m.group(1)] = m.group(2).strip()
        return entries

    def _parse_file(self, root: Path, f: Path, case: ReflexCase, trace: TraceInfo) -> None:
        rel = safe_display_path(f, root)
        text = f.read_text(encoding='utf-8', errors='ignore')
        entries = self._parse_dict_entries(text)
        if rel == 'system/controlDict':
            case.solver_records.append(SolverRecord(application=entries.get('application'), start_time=entries.get('startTime'), end_time=entries.get('endTime'), metadata=entries, trace=trace))
        elif rel in {'system/fvSchemes', 'system/fvSolution'}:
            for key, val in entries.items():
                case.numerical_settings.append(NumericalSettingsRecord(category=Path(rel).name, name=key, value=val, trace=trace))
        elif rel == 'constant/transportProperties':
            for key, val in entries.items():
                case.materials.append(MaterialPropertyRecord(name=key, value=val, trace=trace))
        elif rel == 'constant/turbulenceProperties':
            for key, val in entries.items():
                case.numerical_settings.append(NumericalSettingsRecord(category='turbulenceProperties', name=key, value=val, trace=trace))
        elif rel == 'constant/polyMesh/boundary':
            patches = re.findall(r"\n\s*([A-Za-z0-9_]+)\s*\{\s*type\s+([^;]+);", text)
            for patch, typ in patches:
                case.boundary_conditions.append(BoundaryConditionRecord(patch=patch, type=typ.strip(), trace=trace))
        elif rel.startswith('0/'):
            field_name = Path(rel).name
            cls = entries.get('class') or ('volVectorField' if 'dimensions' in entries else None)
            field_type = FieldType.vector if 'VectorField' in str(cls) or field_name == 'U' else FieldType.scalar
            case.result_fields.append(ResultFieldRecord(name=field_name, association=FieldAssociation.volume, field_type=field_type, trace=trace))
            # boundaryField patch type extraction
            for patch, body in re.findall(r"\n\s*([A-Za-z0-9_]+)\s*\{([^{}]*type\s+[^;]+;[^{}]*)\}", text, flags=re.DOTALL):
                typ = re.search(r"type\s+([^;]+);", body)
                val = re.search(r"value\s+([^;]+);", body)
                case.boundary_conditions.append(BoundaryConditionRecord(patch=patch, field=field_name, type=typ.group(1).strip() if typ else None, value=val.group(1).strip() if val else None, trace=trace))
        if 'Solving for' in text or 'Initial residual' in text:
            case.inspection_flags.append(InspectionFlag(severity=Severity.info, category="residual_like_lines_detected", message=f"Residual-like solver log lines detected in {rel}.", trace=trace))
