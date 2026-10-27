import json
import logging
import subprocess
from pathlib import Path
from time import perf_counter


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "test_config.json"
RESULTS_PATH = BASE_DIR / "results.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    if not isinstance(config, dict):
        raise ValueError("Configuration must be a JSON object")

    if not isinstance(config.get("tests"), list):
        raise ValueError("'tests' must be a list")

    for index, test_case in enumerate(config["tests"]):
        if not isinstance(test_case, dict):
            raise ValueError(f"Test {index} must be an object")

        if not isinstance(test_case.get("name"), str):
            raise ValueError(f"Test {index} needs a string name")

        command = test_case.get("command")
        if (
            not isinstance(command, list)
            or not command
            or not all(isinstance(arg, str) for arg in command)
        ):
            raise ValueError(
                f"Test {index} command must be a non-empty list of strings"
            )

        expected = test_case.get("expected_exit_code")
        if type(expected) is not int:
            raise ValueError(
                f"Test {index} needs an integer expected_exit_code"
            )

        timeout = test_case.get("timeout")
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or timeout <= 0
        ):
            raise ValueError(f"Test {index} needs a positive timeout")

    return config


def run_test(test_case: dict) -> dict:
    name = test_case["name"]
    command = test_case["command"]
    expected_code = test_case["expected_exit_code"]
    timeout = test_case["timeout"]

    logging.info("Starting test: %s", name)
    started = perf_counter()

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )

        duration = perf_counter() - started
        passed = result.returncode == expected_code

        return {
            "name": name,
            "status": "PASS" if passed else "FAIL",
            "expected_exit_code": expected_code,
            "actual_exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration_seconds": round(duration, 3),
        }

    except subprocess.TimeoutExpired:
        duration = perf_counter() - started

        return {
            "name": name,
            "status": "TIMEOUT",
            "expected_exit_code": expected_code,
            "actual_exit_code": None,
            "stdout": "",
            "stderr": f"Timed out after {timeout} seconds",
            "duration_seconds": round(duration, 3),
        }

    except OSError as exc:
        duration = perf_counter() - started

        return {
            "name": name,
            "status": "ERROR",
            "expected_exit_code": expected_code,
            "actual_exit_code": None,
            "stdout": "",
            "stderr": str(exc),
            "duration_seconds": round(duration, 3),
        }


def main():
    try:
        config = load_config(CONFIG_PATH)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        logging.error("Could not load configuration: %s", exc)
        raise SystemExit(1)

    results = [run_test(case) for case in config["tests"]]

    report = {
        "total": len(results),
        "passed": sum(r["status"] == "PASS" for r in results),
        "failed": sum(r["status"] == "FAIL" for r in results),
        "timeouts": sum(r["status"] == "TIMEOUT" for r in results),
        "errors": sum(r["status"] == "ERROR" for r in results),
        "results": results,
    }

    with RESULTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print(json.dumps(report, indent=2))
    logging.info("Report saved to %s", RESULTS_PATH)


if __name__ == "__main__":
    main()
