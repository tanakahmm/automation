
import subprocess
import logging
import json
from time import perf_counter


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def run_diagnosis(name: str, command: list[str]) -> dict:
    started = perf_counter()

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

        return {
            "check": name,
            "status": "PASS" if result.returncode == 0 else "FAIL",
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "duration_seconds": round(
                perf_counter() - started, 3
            ),
        }

    except subprocess.TimeoutExpired:
        logging.error("%s timed out", name)
        return {
            "check": name,
            "status": "TIMEOUT",
            "exit_code": None,
            "stdout": "",
            "stderr": "Command timed out",
            "duration_seconds": round(
                perf_counter() - started, 3
            ),
        }

    except OSError as exc:
        logging.exception("%s could not execute", name)
        return {
            "check": name,
            "status": "ERROR",
            "exit_code": None,
            "stdout": "",
            "stderr": str(exc),
            "duration_seconds": round(
                perf_counter() - started, 3
            ),
        }


def main():
    checks = [
        ("interfaces", ["ip", "addr"]),
        ("routes", ["ip", "route"]),
        ("listening_tcp_ports", ["ss", "-ltn"]),
        ("dns_resolution", ["getent", "hosts", "example.com"]),
    ]

    results = []

    for name, command in checks:
        logging.info("Running diagnostic: %s", name)
        results.append(run_diagnostic(name, command))

    report = {"checks": results}

    with open("network_report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print(json.dumps(report, indent=2))
    logging.info("Report saved to network_report.json")


if __name__ == "__main__":
    main()
