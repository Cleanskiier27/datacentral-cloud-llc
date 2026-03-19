import os
import subprocess
import sys

# This is a lightweight integration test; it runs the fetch script with --sample and ensures output files are created.

def test_sample_fetch(tmp_path):
    outdir = tmp_path / "training_out"
    cmd = [sys.executable, "../training/fetch_xkcd.py", "--start", "401", "--sample", "5", "--chunk-size", "2", "--outdir", str(outdir)]
    # run from repo root
    cwd = os.path.dirname(__file__) + "/.."
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    files = list(outdir.glob("*.jsonl"))
    assert len(files) >= 1
