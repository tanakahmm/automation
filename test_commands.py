import subprocess
import pytest


def run_command(command:list[str],timeout:float=5.0):
    return subprocess.run(command,timeout=timeout,check=False,text=True,capture_output=True)

def test_successful_command():
    result=run_command(["python3","-c","print('test completed')"])
    assert result.returncode==0
    assert "test completed" in result.stdout

def test_failed_command():
    result = run_command([
            "python3",
            "-c",
            "import sys; print('failure', file=sys.stderr); sys.exit(2)",
        ])
    assert result.returncode == 2
    assert "failure" in result.stderr


def test_warning_without_failure():
    result = run_command([
        "python3",
        "-c",
        "import sys; print('warning detected', file=sys.stderr)"
    ])

    assert result.returncode == 0
    assert "warning detected" in result.stderr
    assert result.stdout == ""

def test_command_timeout():
    with pytest.raises(subprocess.TimeoutExpired):
        result = run_command(
            ["python3", "-c", "import time; time.sleep(10)"],
            timeout=1.0,
        )
        print("Result:Timeout after {timeout} seconds ")
