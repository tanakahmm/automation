import pytest

from log_analyzer import analyze_log


def test_analyze_log(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text(
        "INFO service started\n"
        "ERROR connection refused\n"
        "WARNING retrying\n"
        "ERROR connection timeout\n",
        encoding="utf-8",
    )

    report = analyze_log(log_file)

    assert report["total_lines"] == 4
    assert report["counts"]["ERROR"] == 2
    assert report["counts"]["WARNING"] == 1
    assert report["counts"]["TIMEOUT"] == 1
    assert len(report["matches"]) == 3


def test_missing_log_file(tmp_path):
    missing_file = tmp_path / "missing.log"

    with pytest.raises(FileNotFoundError):
        analyze_log(missing_file)


def test_empty_log(tmp_path):
    log_file = tmp_path / "empty.log"
    log_file.write_text("", encoding="utf-8")

    report = analyze_log(log_file)

    assert report["total_lines"] == 0
    assert report["matches"] == []
