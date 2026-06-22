from __future__ import annotations
from pathlib import Path
import re
from caereflex.core.config import CaeReflexConfig
from caereflex.core.fingerprint import sha256_file, stable_case_id
from caereflex.core.models import (
    AdapterResult, AdapterStatus, ReflexCase, CaseType, InspectionStatus, TraceInfo,
    SourceKind, SourceFileRecord, HashStatus, EngineeringAsset, AssetType,
    ResultFieldRecord, FieldAssociation, FieldType, InspectionFlag, Severity, ProvenanceRecord
)
from caereflex.core.provenance import utc_now_iso
from caereflex.core.validation import safe_display_path
from .base import BaseAdapter

class VTKAdapter(BaseAdapter):
    name = "vtk_adapter"
    suffixes = {'.vtk', '.vtu', '.vtp', '.vti', '.vtr', '.vts'}

    def inspect(self, path: str | Path) -> AdapterResult:
        p = Path(path)
        workspace = p.parent if p.is_file() else p
        case = ReflexCase(case_id=stable_case_id(str(p.resolve()) if p.exists() else str(p)), case_name=p.stem if p.is_file() else p.name, case_type=CaseType.vtk,
                          detected_formats=[], detected_tools=['VTK/ParaView-compatible'], physics_tags=['post-processing', 'visualisation data'])
        case.workspace.root_display = safe_display_path(workspace)
        case.provenance.append(ProvenanceRecord(event="vtk_inspection_started", details={"path": safe_display_path(p)}))
        if not p.exists():
            msg = "VTK path not found."
            case.inspection.status = InspectionStatus.failed
            case.inspection_flags.append(InspectionFlag(severity=Severity.error, category="path_not_found", message=msg))
            return AdapterResult(adapter_name=self.name, status=AdapterStatus.failed, case=case, errors=[msg])
        files = [p] if p.is_file() else [x for x in p.rglob('*') if x.is_file() and x.suffix.lower() in self.suffixes]
        for i, f in enumerate(files[: self.config.max_scan_files]):
            sha, hstatus = sha256_file(f, self.config.max_file_size_bytes)
            rel = safe_display_path(f, workspace)
            trace = TraceInfo(source_kind=SourceKind.extracted, source_files=[rel], adapter=self.name)
            case.source_files.append(SourceFileRecord(file_id=f"file_{i+1}", relative_path=rel, suffix=f.suffix.lower(), size_bytes=f.stat().st_size, sha256=sha, hash_status=HashStatus(hstatus), trace=trace))
            case.detected_formats.append(f.suffix.lower())
            asset = EngineeringAsset(asset_id=f"asset_{len(case.assets)+1}", asset_type=AssetType.result_file, name=f.name, trace=trace)
            if f.suffix.lower() == '.vtk':
                self._inspect_legacy_vtk(f, case, asset, trace)
            else:
                case.inspection_flags.append(InspectionFlag(severity=Severity.info, category="extra_backed_vtk", message=f"{f.suffix} fingerprinted. Install [vtk] for deeper inspection.", trace=trace))
            case.assets.append(asset)
        if not case.source_files:
            msg = "No VTK-compatible files detected."
            case.inspection.status = InspectionStatus.failed
            case.inspection_flags.append(InspectionFlag(severity=Severity.error, category="unsupported_format", message=msg))
            return AdapterResult(adapter_name=self.name, status=AdapterStatus.unsupported, case=case, errors=[msg])
        case.detected_formats = sorted(set(case.detected_formats))
        case.inspection.status = InspectionStatus.partial_success if case.inspection_flags else InspectionStatus.success
        case.inspection.completed_at = utc_now_iso()
        case.agent_summary.summary = f"VTK-compatible result data inspected with {len(case.source_files)} file(s)."
        case.agent_summary.do_not_claim = ["Do not claim derived-field physics.", "Do not claim validation or design safety."]
        return AdapterResult(adapter_name=self.name, status=AdapterStatus(case.inspection.status.value), case=case)

    def _inspect_legacy_vtk(self, f: Path, case: ReflexCase, asset: EngineeringAsset, trace: TraceInfo) -> None:
        text = f.read_text(encoding='utf-8', errors='ignore')[:200000]
        dataset = re.search(r"DATASET\s+(\S+)", text)
        points = re.search(r"POINTS\s+(\d+)", text)
        cells = re.search(r"CELLS\s+(\d+)", text)
        asset.metrics.update({
            "dataset_type": dataset.group(1) if dataset else None,
            "points": int(points.group(1)) if points else None,
            "cells": int(cells.group(1)) if cells else None,
        })
        for name in re.findall(r"SCALARS\s+(\S+)", text):
            case.result_fields.append(ResultFieldRecord(name=name, association=FieldAssociation.point, field_type=FieldType.scalar, components=1, trace=trace))
        for name in re.findall(r"VECTORS\s+(\S+)", text):
            case.result_fields.append(ResultFieldRecord(name=name, association=FieldAssociation.point, field_type=FieldType.vector, components=3, trace=trace))
