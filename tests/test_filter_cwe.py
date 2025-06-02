import subprocess
import os
import re

SCRIPT = "filter_cwe.py"

def test_or_mode_java():
    outfile = "test_java_output.txt"
    result = subprocess.run(
        ["python", SCRIPT, "--languages", "Java", "--output", outfile],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    with open(outfile, "r", encoding="utf-8") as f:
        content = f.read().lower()
        assert "java" in content
    os.remove(outfile)

def test_or_mode_multiple_languages():
    outfile = "test_multilang_output.txt"
    result = subprocess.run(
        ["python", SCRIPT, "--languages", "Java,Python", "--output", outfile],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    with open(outfile, "r", encoding="utf-8") as f:
        content = f.read().lower()
        assert "java" in content or "python" in content
    os.remove(outfile)

def test_and_mode():
    outfile = "test_and_output.txt"
    result = subprocess.run(
        ["python", SCRIPT, "--languages", "Java,Python", "--mode", "and", "--output", outfile],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    with open(outfile, "r", encoding="utf-8") as f:
        content = f.read().lower()
        if content.strip() and "cwe-id:" in content:
            entries = content.split("cwe-id:")
            for entry in entries:
                if entry.strip():
                    m = re.search(r"applicable platforms:(.*)\n", entry)
                    if m:
                        platforms = m.group(1).lower()
                        assert "java" in platforms and "python" in platforms
    os.remove(outfile)

def test_no_match_language():
    outfile = "test_nomatch_output.txt"
    result = subprocess.run(
        ["python", SCRIPT, "--languages", "TotallyFakeLang", "--output", outfile],
        capture_output=True, text=True
    )
    # output to stderr
    assert "no records found" in result.stderr.lower()
    if os.path.exists(outfile):
        os.remove(outfile)

def test_invalid_argument():
    result = subprocess.run(
        ["python", SCRIPT],
        capture_output=True, text=True
    )
    assert result.returncode != 0  # for missing parameters
