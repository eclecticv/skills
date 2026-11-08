import json
import importlib.util
from pathlib import Path

def _load():
    p = Path(__file__).parent.parent / "scripts" / "capture_session.py"
    spec = importlib.util.spec_from_file_location("capture_session", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

cs = _load()

def test_detect_signals_finds_shipped_and_fixed():
    text = "We shipped the feature after we fixed the crash."
    assert cs.detect_signals(text) == ["fixed", "shipped"]

def test_detect_signals_empty_when_none():
    assert cs.detect_signals("just renamed a few variables") == []

def test_build_digest_extracts_repo_from_cwd():
    d = cs.build_digest({"session_id": "abc", "cwd": "/home/u/Developer/myrepo"}, "we shipped it")
    assert d["repo"] == "myrepo"
    assert d["session_id"] == "abc"
    assert d["signals"] == ["shipped"]

def test_build_digest_falls_back_to_process_cwd_when_absent():
    import os
    d = cs.build_digest({"session_id": "x"}, "shipped it")
    assert d["cwd"] == os.getcwd()
    assert d["repo"] == os.path.basename(os.getcwd())


def test_append_journal_writes_one_line_each(tmp_path):
    jp = tmp_path / "journal.jsonl"
    cs.append_journal({"ts": "x", "signals": ["shipped"]}, path=jp)
    cs.append_journal({"ts": "y", "signals": []}, path=jp)
    lines = jp.read_text().strip().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["signals"] == ["shipped"]
