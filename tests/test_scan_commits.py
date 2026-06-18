import importlib.util
import subprocess
from pathlib import Path

def _load():
    p = Path(__file__).parent.parent / "scripts" / "scan_commits.py"
    spec = importlib.util.spec_from_file_location("scan_commits", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

sc = _load()

def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)

def _make_repo(tmp_path):
    repo = tmp_path / "demo-repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "Tester")
    (repo / "f.txt").write_text("a")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "ship: release v1.2")
    return repo

def test_signals_for_detects_ship():
    assert "shipped" in sc.signals_for("ship: release v1.2")

def test_signals_for_detects_fix():
    assert "fixed" in sc.signals_for("fix: null pointer in parser")

def test_scan_returns_commit_with_signal(tmp_path):
    repo = _make_repo(tmp_path)
    commits = sc.scan([str(repo)], "1 year ago")
    assert len(commits) == 1
    assert commits[0]["subject"] == "ship: release v1.2"
    assert commits[0]["repo"] == "demo-repo"
    assert "shipped" in commits[0]["signals"]

def test_scan_nonexistent_repo_is_empty():
    assert sc.scan(["/no/such/repo/here"], "1 year ago") == []
