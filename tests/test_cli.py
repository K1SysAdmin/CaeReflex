from typer.testing import CliRunner
from caereflex.cli.main import app

runner = CliRunner()

def test_cli_version():
    result = runner.invoke(app, ['version'])
    assert result.exit_code == 0
    assert '1.0.0' in result.output

def test_examples_list():
    result = runner.invoke(app, ['examples', 'list'])
    assert result.exit_code == 0
    assert 'openfoam_cavity_minimal' in result.output
