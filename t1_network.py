import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import perf_counter


def check_tcp(endpoint: tuple[str, int], timeout: float = 2.0) -> dict:
    host, port = endpoint
    started = perf_counter()

    try:
        with socket.create_connection(
            (host, port),
            timeout=timeout,
        ):
            status = "PASS"
            error = None

    except ConnectionRefusedError:
        status = "REFUSED"
        error = "Connection refused"

    except TimeoutError:
        status = "TIMEOUT"
        error = "Connection timed out"

    except OSError as exc:
        status = "ERROR"
        error = str(exc)

    return {
        "host": host,
        "port": port,
        "status": status,
        "error": error,
        "duration_seconds": round(perf_counter() - started, 3),
    }


def check_many(
    endpoints: list[tuple[str, int]],
    max_workers: int = 5,
) -> list[dict]:
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")

    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(check_tcp, endpoint): endpoint
            for endpoint in endpoints
        }

        for future in as_completed(futures):
            endpoint = futures[future]

            try:
                results.append(future.result())
            except Exception as exc:
                # Preserve unexpected worker errors for diagnosis.
                results.append({
                    "host": endpoint[0],
                    "port": endpoint[1],
                    "status": "ERROR",
                    "error": f"Unexpected worker error: {exc}",
                })

    return results


if __name__ == "__main__":
    endpoints = [
        ("127.0.0.1", 5000),
        ("127.0.0.1", 5001),
        ("127.0.0.1", 5002),
    ]

    for result in check_many(endpoints):
        print(result)
