from unittest.mock import patch

from health_checker import check_tcp_with_retries


def test_retry_then_success():
    refused = {
        "status": "REFUSED",
        "host": "127.0.0.1",
        "port": 5000,
        "duration_seconds": 0.01,
        "error": "Connection refused",
    }

    success = {
        "status": "PASS",
        "host": "127.0.0.1",
        "port": 5000,
        "duration_seconds": 0.01,
        "error": None,
    }

    with patch(
        "health_checker.check_tcp",
        side_effect=[refused, refused, success],
    ) as mock_check:
        result = check_tcp_with_retries(
            "127.0.0.1",
            5000,
            attempts=3,
            delay=0,
        )

    assert result["status"] == "PASS"
    assert result["attempts_used"] == 3
    assert mock_check.call_count == 3


def test_all_attempts_fail():
    refused = {
        "status": "REFUSED",
        "host": "127.0.0.1",
        "port": 5000,
        "duration_seconds": 0.01,
        "error": "Connection refused",
    }

    with patch(
        "health_checker.check_tcp",
        return_value=refused,
    ) as mock_check:
        result = check_tcp_with_retries(
            "127.0.0.1",
            5000,
            attempts=3,
            delay=0,
        )

    assert result["status"] == "REFUSED"
    assert result["attempts_used"] == 3
    assert mock_check.call_count == 3
