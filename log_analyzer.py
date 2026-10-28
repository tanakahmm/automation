
import json
import logging
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def analyze_log(log_path: Path) -> dict:
    if not log_path.is_file():
        raise FileNotFoundError(f"Log file not found: {log_path}")

    counts = {
        "ERROR": 0,
        "WARNING": 0,
        "TIMEOUT": 0,
        "FAILED": 0,
        "EXCEPTION": 0,
    }

    matches = []

    with log_path.open("r", encoding="utf-8", errors="replace") as file:
        for line_number, line in enumerate(file, start=1):
            upper_line = line.upper()
            found = []

            for keyword in counts:
                if keyword in upper_line:
                    counts[keyword] += 1
                    found.append(keyword)

            if found:
                matches.append({
                    "line_number": line_number,
                    "keywords": found,
                    "message": line.rstrip(),
                })

    report = {
        "file": str(log_path),
        "total_lines": line_number if "line_number" in locals() else 0,
        "counts": counts,
        "matches": matches,
    }

    logging.info("Analyzed %s", log_path)
    return report


if __name__ == "__main__":
    report = analyze_log(Path("sample_app.log"))

    print(json.dumps(report, indent=2))

    Path("diagnostic_report.json").write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )
