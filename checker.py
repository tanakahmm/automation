import logging
import socket
from time import perf_counter


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def check_tcp(
    host: str,
    port: int,
    timeout: float = 3.0,
) -> dict:
    started = perf_counter()

    logging.info(
        "Checking TCP service at %s:%d",
        host,
        port,
    )

    try:
        with socket.create_connection(
            (host, port),
            timeout=timeout,
        ):
            duration = perf_counter() - started

            logging.info("Connection successful")

            return {
                "host": host,
                "port": port,
                "status": "PASS",
                "duration_seconds": round(duration, 3),
                "error": None,
            }

    except ConnectionRefusedError:
        error = "Connection refused"
        status = "REFUSED"

    except TimeoutError:
        error = "Connection timed out"
        status = "TIMEOUT"

    except OSError as exc:
        error = str(exc)
        status = "ERROR"

    duration = perf_counter() - started

    logging.error(
        "TCP check failed: %s",
        error,
    )

    return {
        "host": host,
        "port": port,
        "status": status,
        "duration_seconds": round(duration, 3),
        "error": error,
    }


if __name__ == "__main__":
    result = check_tcp("127.0.0.1", 5000)
    print(result)
