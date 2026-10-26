import logging
import subprocess
from time import perf_counter


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def run_command(command: list[str], timeout: float = 5.0):
    started = perf_counter()

    logging.info("Starting command: %s", command)

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )

        duration = perf_counter() - started

        if result.stdout.strip():
            logging.info("STDOUT: %s", result.stdout.strip())

        if result.stderr.strip():
            logging.warning("STDERR: %s", result.stderr.strip())

        if result.returncode == 0:
            logging.info(
                "Command passed in %.3f seconds",
                duration,
            )
        else:
            logging.error(
                "Command failed with exit code %d in %.3f seconds",
                result.returncode,
                duration,
            )

        return result.returncode

    except subprocess.TimeoutExpired:
        logging.error("Command timed out after %.1f seconds", timeout)
        return None

    except OSError:
        logging.exception("Unable to execute command")
        return None


if __name__ == "__main__":
    exit_code = run_command([
        "python3", "-c", "print('Automation started')"
    ])

    print("Final exit code:", exit_code)
