import time
import logging
from checker import check_tcp


def check_tcp_with_retries(
    host: str,
    port: int,
    attempts: int = 3,
    timeout: float = 2.0,
    delay: float = 1.0,
) -> dict:
    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    if timeout <= 0:
        raise ValueError("timeout must be positive")

    if delay < 0:
        raise ValueError("delay cannot be negative")

    last_result = None

    for attempt in range(1, attempts + 1):
        logging.info(
            "Attempt %d of %d for %s:%d",
            attempt,
            attempts,
            host,
            port,
        )

        result = check_tcp(host, port)
        last_result = result

        if result["status"] == "PASS":
            result["attempts_used"] = attempt
            return result

        if attempt < attempts:
            logging.warning("Attempt failed; retrying in %.1f seconds", delay)
            time.sleep(delay)

    last_result["attempts_used"] = attempts
    return last_result
