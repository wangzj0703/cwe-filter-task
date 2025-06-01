import subprocess
import os
import re

SCRIPT = "filter_cwe.py"

def test_or_mode_java():
    """Test OR mode: filtering for Java (should match lines mentioning Java)"""
    result = subprocess.run(
        ["python", SCRIPT, "--languages", "Java"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    # 检查输出是否包含java，不区分大小写
    assert "java" in result.stdout.lower()

def test_or_mode_multiple_languages():
    """Test OR mode: filtering for Java and Python (should match any)"""
    result = subprocess.run(
        ["python", SCRIPT, "--languages", "Java,Python"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    # 只要有一个就通过
    assert "java" in result.stdout.lower() or "python" in result.stdout.lower()

def test_and_mode():
    """Test AND mode: only match CWEs that mention BOTH Java and Python"""
    result = subprocess.run(
        ["python", SCRIPT, "--languages", "Java,Python", "--mode", "and"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    # 如果输出非空，每条都应同时含有java和python
    output = result.stdout.lower()
    if output.strip() and "cwe-id:" in output:
        # 拆分多条输出
        entries = output.split("cwe-id:")
        for entry in entries:
            if entry.strip():
                m = re.search(r"applicable platforms:(.*)\n", entry)
                if m:
                    platforms = m.group(1).lower()
                    assert "java" in platforms and "python" in platforms

def test_no_match_language():
    """Test for a language unlikely to be present"""
    result = subprocess.run(
        ["python", SCRIPT, "--languages", "TotallyFakeLang"],
        capture_output=True, text=True
    )
    # 应该输出 no records found
    assert "no records found" in result.stderr.lower()

def test_invalid_argument():
    """Test for missing languages argument (should error)"""
    result = subprocess.run(
        ["python", SCRIPT],
        capture_output=True, text=True
    )
    assert result.returncode != 0  # 参数缺失时应该报错

# 可继续加其它边界/健壮性测试
