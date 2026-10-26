import subprocess
from unittest.mock import patch, Mock

def check_device():
    result = subprocess.run(
        ["ping", "-c", "1", "192.0.2.10"],
        capture_output=True,
        text=True,
        timeout=3,
    )
    return result.returncode == 0


def test_device_reachable():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = Mock(returncode=0)

        result = check_device()

        assert result is True
        mock_run.assert_called_once()
