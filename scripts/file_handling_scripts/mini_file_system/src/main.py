import os
import logging
import argparse
from pathlib import Path

from src.utils.path_manager import PathManager
from src.utils.file_scanner import FileScanner
from src.utils.config_loader import load_config
from src.utils.report_writer import ReportWriter

# ── Project root resolution (computed once at module level) ──────────────
# main.py lives at:  mini_file_system/src/main.py
# .parent         =  mini_file_system/src/
# .parent         =  mini_file_system/            ← project root ✓
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def setup_logging(level_str: str) -> None:
    """Configure root logger with file + console handlers.
    Log file goes to mini_file_system/logs/app.log (project root).
    """
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    level = getattr(logging, level_str.upper(), logging.DEBUG)
    logging.basicConfig(
        level=level,
        format="%(asctime)s — %(levelname)s — %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "app.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mini File System Scanner")
    parser.add_argument("--folder",       type=str, help="Override target folder from config")
    parser.add_argument("--threshold_mb", type=int, help="Override large-file threshold (MB)")
    parser.add_argument("--report",       type=str, default="scan_report.md",
                        help="Output report filename (default: scan_report.md)")
    return parser.parse_args()


def main() -> None:

    # ── Load config from mini_file_system/config/config.json ────────
    config = load_config(str(PROJECT_ROOT / "config" / "config.json"))

    # ── Setup logging before any logging calls ───────────────────────
    setup_logging(config["log_level"])

    logging.debug(f"Project root : {PROJECT_ROOT}")
    logging.debug(f"CWD          : {os.getcwd()}")

    # ── CLI overrides ────────────────────────────────────────────────
    args = parse_args()
    target_folder_name: str = args.folder or config["target_folder"]
    threshold_mb: int       = args.threshold_mb or config["large_file_threshold_mb"]

    # ── Resolve target folder relative to project root ───────────────
    # "data"  ->  mini_file_system/data/   (never src/data)
    target_folder = PathManager.resolve_path(PROJECT_ROOT, target_folder_name)
    logging.debug(f"Target folder: {target_folder}")

    PathManager.ensure_exists(target_folder, expected_type="dir", create_if_missing=True)

    # ── Scan ─────────────────────────────────────────────────────────
    scanner = FileScanner(target_folder, threshold_mb)

    for meta in scanner.scan():
        if meta is not None:   # None = file failed extraction (already logged)
            logging.info(meta)

    scanner.report_duplicates()
    scanner.report_summary()

    # ── Write report to mini_file_system/reports/ ────────────────────
    scan_summary = scanner.get_summary()
    reports_dir  = str(PROJECT_ROOT / "reports")
    writer        = ReportWriter(reports_dir)
    out_path      = writer.write_report(scan_summary, filename=args.report)

    logging.info(f"Report saved : {out_path}")


if __name__ == "__main__":
    main()