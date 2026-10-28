import os
import subprocess
import logging
from time import perf_counter


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def inspect_process(pid: int) -> dict:
    if pid <= 0:
        raise ValueError("PID must be positive")

    command = [
        "ps",
        "-p", str(pid),
        "-o", "pid=,ppid=,stat=,%cpu=,%mem=,comm=",
    ]

    started = perf_counter()

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
    except subprocess.TimeoutExpired:
        logging.error("Process inspection timed out")
        return {"status": "TIMEOUT", "pid": pid}
    except OSError:
        logging.exception("Unable to execute ps")
        return {"status": "ERROR", "pid": pid}

    duration = perf_counter() - started

    if result.returncode != 0:
        logging.error("ps failed: %s", result.stderr.strip())
        return {
            "status": "ERROR",
            "pid": pid,
            "error": result.stderr.strip(),
        }

    output = result.stdout.strip()

    if not output:
        return {
            "status": "NOT_FOUND",
            "pid": pid,
            "duration_seconds": round(duration, 3),
        }

    logging.info("Process inspected successfully")

    return {
        "status": "FOUND",
        "pid": pid,
        "details": output,
        "duration_seconds": round(duration, 3),
    }


def check_service(service_name: str) -> dict:
    if not service_name or service_name.startswith("-"):
        raise ValueError("Invalid service name")

    try:
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {
            "service": service_name,
            "status": "TIMEOUT",
        }
    except OSError as exc:
        return {
            "service": service_name,
            "status": "ERROR",
            "error": str(exc),
        }

    active_state = result.stdout.strip()

    return {
        "service": service_name,
        "status": "ACTIVE" if result.returncode == 0 else "INACTIVE",
        "reported_state": active_state,
        "returncode": result.returncode,
    }


if __name__ == "__main__":
    current_pid = os.getpid()
    print(inspect_process(current_pid))
    print(check_service("ssh"))