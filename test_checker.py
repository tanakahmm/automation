import socket

from checker import check_tcp


def test_tcp_service_reachable():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        port = server.getsockname()[1]

        result = check_tcp("127.0.0.1", port)

        assert result["status"] == "PASS"
        assert result["port"] == port
        assert result["duration_seconds"] >= 0


def test_tcp_service_refused():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("127.0.0.1", 0))
        port = server.getsockname()[1]

    result = check_tcp("127.0.0.1", port, timeout=1.0)

    assert result["status"] == "REFUSED"
    assert result["error"] == "Connection refused"
