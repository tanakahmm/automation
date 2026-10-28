
import os
from unittest.mock import patch

from linux_monitoring import inspect_process, check_service


def test_inspect_current_process():
    result = inspect_process(os.getpid())

    assert result["status"] == "FOUND"
    assert result["pid"] == os.getpid()
    assert "details" in result


def test_invalid_pid():
    import pytest

    with pytest.raises(ValueError):
        inspect_process(-1)


def test_active_service():
    with patch("linux_monitoring.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "active\n"
        mock_run.return_value.stderr = ""

        result = check_service("example.service")

    assert result["status"] == "ACTIVE"
    assert result["reported_state"] == "active"


def test_inactive_service():
    with patch("linux_monitoring.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 3
        mock_run.return_value.stdout = "inactive\n"
        mock_run.return_value.stderr = ""

        result = check_service("example.service")

    assert result["status"] == "INACTIVE"
