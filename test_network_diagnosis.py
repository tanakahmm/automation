from unittest.mock import patch, Mock

from network_diagnosis import run_diagnosis


def test_diagnostic_command_success():
    mock_result = Mock(
        returncode=0,
        stdout="127.0.0.1",
        stderr="",
    )

    with patch(
        "network_diagnosis.subprocess.run",
        return_value=mock_result,
    ):
        result = run_diagnosis(
            "test_dns",
            ["getent", "hosts", "example.com"],
        )

    assert result["status"] == "PASS"
    assert result["stdout"] == "127.0.0.1"


def test_diagnostic_command_failure():
    mock_result = Mock(
        returncode=2,
        stdout="",
        stderr="invalid command",
    )

    with patch(
        "network_diagnosis.subprocess.run",
        return_value=mock_result,
    ):
        result = run_diagnosis(
            "test",
            ["some-command"],
        )

    assert result["status"] == "FAIL"
    assert result["exit_code"] == 2


def test_diagnostic_timeout():
    import subprocess
    import pytest

    with patch(
        "network_diagnosis.subprocess.run",
        side_effect=subprocess.TimeoutExpired("ip", 5),
    ):
        result = run_diagnosis("interfaces", ["ip", "addr"])

    assert result["status"] == "TIMEOUT"
