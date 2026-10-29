from unittest.mock import patch

from t1_network import check_many


def test_check_many_collects_results():
    fake_results = [
        {
            "host": "127.0.0.1",
            "port": 5000,
            "status": "PASS",
            "error": None,
            "duration_seconds": 0.01,
        },
        {
            "host": "127.0.0.1",
            "port": 5001,
            "status": "REFUSED",
            "error": "Connection refused",
            "duration_seconds": 0.01,
        },
    ]

    with patch(
        "t1_network.check_tcp",
        side_effect=fake_results,
    ) as mock_check:
        results = check_many(
            [("127.0.0.1", 5000), ("127.0.0.1", 5001)],
            max_workers=2,
        )

    assert len(results) == 2
    assert {r["status"] for r in results} == {"PASS", "REFUSED"}
    assert mock_check.call_count == 2
