from __future__ import annotations
from pathlib import Path
import json, os, sys
import typer
from rich.console import Console
from caereflex.version import __version__
from caereflex.core.config import CaeReflexConfig
from caereflex.core.errors import CaeReflexError, DependencyMissingError, PathSafetyError, UnsupportedFormatError
from caereflex.services import inspect_path, save_case, export_case, attach_crossref, search_crossref, run_example, list_examples

app = typer.Typer(help="CaeReflex: agent-readable engineering evidence for simulation artefacts.")
crossref_app = typer.Typer(help="CrossRef metadata commands.")
export_app = typer.Typer(help="Export commands.")
examples_app = typer.Typer(help="Bundled examples.")
app.add_typer(crossref_app, name="crossref")
app.add_typer(export_app, name="export")
app.add_typer(examples_app, name="examples")
console = Console()

EXIT = {"success": 0, "failed": 1, "partial_success": 2, "unsupported": 3, "dependency": 4, "security": 5}

def _status_value(status):
    return status.value if hasattr(status, 'value') else str(status)

def _print_result(data: dict, json_mode: bool = False):
    if json_mode:
        typer.echo(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        console.print(f"[bold]Status:[/bold] {data.get('status')}")
        if data.get('case_id'): console.print(f"[bold]Case ID:[/bold] {data.get('case_id')}")
        if data.get('summary'): console.print(data.get('summary'))
        if data.get('outputs'):
            console.print("[bold]Outputs:[/bold]")
            for k, v in data['outputs'].items(): console.print(f"- {k}: {v}")
        if data.get('warnings'):
            console.print("[bold yellow]Warnings:[/bold yellow]")
            for w in data['warnings']: console.print(f"- {w}")

def _exit_for(status: str):
    if status == 'success': raise typer.Exit(0)
    if status == 'partial_success': raise typer.Exit(2)
    raise typer.Exit(1)

@app.command("version")
def version():
    """Print CaeReflex version."""
    typer.echo(__version__)

@app.command("inspect")
def inspect_cmd(path: Path, out: Path = typer.Option(Path('caereflex.json')), agent_context: Path | None = typer.Option(None), report: Path | None = typer.Option(None), attach_crossref_flag: bool = typer.Option(False, "--attach-crossref"), crossref_limit: int = 10, json_mode: bool = typer.Option(False, "--json"), max_file_size_mb: int = 25, max_scan_depth: int = 3, max_scan_files: int = 500):
    """Inspect a simulation path using adapter auto-detection."""
    cfg = CaeReflexConfig(max_file_size_mb=max_file_size_mb, max_scan_depth=max_scan_depth, max_scan_files=max_scan_files)
    case = inspect_path(path, config=cfg, attach_crossref=attach_crossref_flag, crossref_kwargs={"limit": crossref_limit})
    save_case(case, out)
    outputs = {"caereflex_json": str(out)}
    if agent_context:
        export_case(case, 'agent-context', agent_context); outputs['agent_context'] = str(agent_context)
    if report:
        export_case(case, 'markdown', report); outputs['report'] = str(report)
    data = {"status": _status_value(case.inspection.status), "case_id": case.case_id, "summary": case.agent_summary.summary, "outputs": outputs, "warnings": [f.message for f in case.inspection_flags]}
    _print_result(data, json_mode); _exit_for(data['status'])

@app.command("inspect-gmsh")
def inspect_gmsh(path: Path, out: Path = typer.Option(Path('gmsh_case.json')), json_mode: bool = typer.Option(False, "--json")):
    case = inspect_path(path, adapter='gmsh'); save_case(case, out)
    data = {"status": _status_value(case.inspection.status), "case_id": case.case_id, "summary": case.agent_summary.summary, "outputs": {"caereflex_json": str(out)}, "warnings": [f.message for f in case.inspection_flags]}
    _print_result(data, json_mode); _exit_for(data['status'])

@app.command("inspect-openfoam")
def inspect_openfoam(path: Path, out: Path = typer.Option(Path('openfoam_case.json')), json_mode: bool = typer.Option(False, "--json")):
    case = inspect_path(path, adapter='openfoam'); save_case(case, out)
    data = {"status": _status_value(case.inspection.status), "case_id": case.case_id, "summary": case.agent_summary.summary, "outputs": {"caereflex_json": str(out)}, "warnings": [f.message for f in case.inspection_flags]}
    _print_result(data, json_mode); _exit_for(data['status'])

@app.command("inspect-vtk")
def inspect_vtk(path: Path, out: Path = typer.Option(Path('vtk_case.json')), json_mode: bool = typer.Option(False, "--json")):
    case = inspect_path(path, adapter='vtk'); save_case(case, out)
    data = {"status": _status_value(case.inspection.status), "case_id": case.case_id, "summary": case.agent_summary.summary, "outputs": {"caereflex_json": str(out)}, "warnings": [f.message for f in case.inspection_flags]}
    _print_result(data, json_mode); _exit_for(data['status'])

@crossref_app.command("search")
def crossref_search(case_json: Path, query: str | None = None, include_case_tags: bool = True, limit: int = 10, mailto: str | None = None, mock_response: Path | None = typer.Option(None), out: Path | None = None, json_mode: bool = typer.Option(False, "--json")):
    from caereflex.services import load_case
    case = load_case(case_json)
    records, ctx = search_crossref(case, query=query, include_case_tags=include_case_tags, limit=limit, mailto=mailto, mock_response=mock_response)
    data = {"status": "success", "queries": ctx.queries, "records": [r.model_dump(mode='json') for r in records], "literature_context": ctx.model_dump(mode='json')}
    if out:
        out.write_text(json.dumps(data, indent=2), encoding='utf-8')
    _print_result({"status":"success", "summary": f"CrossRef search returned {len(records)} record(s).", "outputs": {"json": str(out)} if out else {}}, json_mode)

@crossref_app.command("attach")
def crossref_attach(case_json: Path, query: str | None = None, include_case_tags: bool = True, limit: int = 10, mailto: str | None = None, mock_response: Path | None = typer.Option(None), out: Path = typer.Option(Path('caereflex.with_literature.json')), json_mode: bool = typer.Option(False, "--json")):
    case = attach_crossref(case_json, query=query, include_case_tags=include_case_tags, limit=limit, mailto=mailto, mock_response=mock_response)
    save_case(case, out)
    data = {"status": "success", "case_id": case.case_id, "summary": case.literature_context.summary, "outputs": {"caereflex_json": str(out)}, "warnings": [f.message for f in case.inspection_flags]}
    _print_result(data, json_mode)

@export_app.command("agent-context")
def export_agent_context(case_json: Path, out: Path = typer.Option(Path('agent_context.json')), json_mode: bool = typer.Option(False, "--json")):
    export_case(case_json, 'agent-context', out)
    _print_result({"status": "success", "outputs": {"agent_context": str(out)}}, json_mode)

@export_app.command("markdown")
def export_markdown(case_json: Path, out: Path = typer.Option(Path('case_report.md')), json_mode: bool = typer.Option(False, "--json")):
    export_case(case_json, 'markdown', out)
    _print_result({"status": "success", "outputs": {"report": str(out)}}, json_mode)

@export_app.command("bibtex")
def export_bibtex(case_json: Path, out: Path = typer.Option(Path('references.bib')), json_mode: bool = typer.Option(False, "--json")):
    export_case(case_json, 'bibtex', out)
    _print_result({"status": "success", "outputs": {"bibtex": str(out)}}, json_mode)

@app.command("serve")
def serve(host: str = "127.0.0.1", port: int = 8765, workspace: Path = Path('.'), api_key: str | None = None, max_request_body_mb: int = 10, max_file_size_mb: int = 25, max_scan_depth: int = 3, max_scan_files: int = 500):
    """Start the REST/OpenAPI server."""
    if host not in {"127.0.0.1", "localhost"} and not api_key:
        console.print("[red]API key is mandatory outside localhost.[/red]")
        raise typer.Exit(5)
    try:
        import uvicorn
        from caereflex.server.app import create_app
    except Exception as e:
        console.print(f"[red]Install [server] extras to run the REST server: {e}[/red]")
        raise typer.Exit(4)
    app_obj = create_app(workspace=workspace, api_key=api_key, host=host)
    console.print("CaeReflex server running.")
    console.print(f"Mode: {'localhost' if host in {'127.0.0.1','localhost'} else 'external'}")
    console.print(f"Workspace: {workspace}")
    console.print(f"OpenAPI: http://{host}:{port}/openapi.json")
    uvicorn.run(app_obj, host=host, port=port)

@examples_app.command("list")
def examples_list(json_mode: bool = typer.Option(False, "--json")):
    names = list_examples()
    if json_mode:
        typer.echo(json.dumps({"examples": names}, indent=2))
    else:
        for n in names: typer.echo(n)

@examples_app.command("run")
def examples_run(name: str, out_dir: Path = Path('build'), json_mode: bool = typer.Option(False, "--json")):
    data = run_example(name, out_dir=out_dir)
    _print_result(data, json_mode)

if __name__ == "__main__":
    app()
