import importlib.util
from pathlib import Path

def _load():
    p = Path(__file__).parent.parent / "scripts" / "secret_scan.py"
    spec = importlib.util.spec_from_file_location("secret_scan", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ss = _load()

def test_scan_detects_openai_key():
    f = ss.scan("here is my key sk-abcdefghij1234567890XYZ token")
    assert any(x["type"] == "openai_key" for x in f)

def test_scan_detects_aws_key():
    assert any(x["type"] == "aws_access_key" for x in ss.scan("AKIAIOSFODNN7EXAMPLE in code"))

def test_scan_flags_denylist_case_insensitive():
    f = ss.scan("We helped AcmeCorp ship", denylist=["acmecorp"])
    assert any(x["type"] == "denylist" for x in f)

def test_scan_clean_text_returns_empty():
    assert ss.scan("Shipped a clean caching layer today. No secrets here.") == []

def test_entropy_of_repeated_char_is_zero():
    assert ss.shannon_entropy("aaaa") == 0.0
