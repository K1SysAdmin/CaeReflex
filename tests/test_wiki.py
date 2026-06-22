import subprocess
import sys
from pathlib import Path


def test_wiki_release_controls_are_enforced():
    result = subprocess.run(
        [sys.executable, "wiki/scripts/validate_wiki.py"],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
