from pathlib import Path
from caereflex.core.fingerprint import sha256_file

def test_sha256(tmp_path):
    p = tmp_path/'a.txt'; p.write_text('abc')
    h,s = sha256_file(p)
    assert s == 'complete' and h
