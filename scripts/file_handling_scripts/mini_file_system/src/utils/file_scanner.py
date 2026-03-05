import os
import logging
from collections import defaultdict
from typing import Dict, Generator, Optional
from datetime import datetime


class FileScanner:
    """
    Walks a directory tree, extracts file metadata, and tracks scan statistics.

    Counters:
        total_discovered : every file os.walk sees
        total_processed  : files successfully extracted
        total_failed     : files that raised an exception during extraction
    """

    def __init__(self, root_path: str, large_file_threshold_mb: int = 10) -> None:
        self.root_path = root_path
        self.large_file_threshold_bytes = large_file_threshold_mb * 1024 * 1024

        # Counters
        self.total_discovered: int = 0
        self.total_processed: int = 0
        self.total_failed: int = 0

        # Metrics
        self.extension_count: Dict[str, int] = defaultdict(int)
        self.large_files: list[str] = []
        self.duplicates: Dict[str, list[str]] = defaultdict(list)

    # ------------------------------------------------------------------
    # MAIN SCAN LOOP
    # ------------------------------------------------------------------
    def scan(self) -> Generator[Optional[Dict], None, None]:
        """
        Yield metadata dicts for each successfully processed file.
        Failed files yield None so callers can count/log them if needed.
        After the walk completes, counter integrity is verified.
        """
        for root, _, files in os.walk(self.root_path):
            for filename in files:
                full_path = os.path.join(root, filename)
                self.total_discovered += 1

                try:
                    meta = self._extract_metadata(full_path)
                    self.total_processed += 1
                    yield meta

                except Exception as e:
                    self.total_failed += 1
                    logging.error(f"[FAILED] {full_path} → {e}")
                    yield None  # explicit None so callers know a file was skipped

        self._verify_counters()

    # ------------------------------------------------------------------
    # METADATA EXTRACTION
    # ------------------------------------------------------------------
    def _extract_metadata(self, path: str) -> Dict:
        """
        Extract metadata from a single file.
        Raises RuntimeError for simulated failures (filename contains 'fail').
        """
        if "fail" in os.path.basename(path).lower():
            raise RuntimeError("Simulated failure — filename contains 'fail'")

        size = os.path.getsize(path)
        ext = os.path.splitext(path)[1] or "<no-ext>"
        modified = datetime.fromtimestamp(os.path.getmtime(path)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Extension tracking
        self.extension_count[ext] += 1

        # Size warnings
        if size == 0:
            logging.warning(f"Zero-byte file detected: {path}")
        elif size > self.large_file_threshold_bytes:
            threshold_mb = self.large_file_threshold_bytes // (1024 * 1024)
            logging.warning(
                f"Large file (>{threshold_mb} MB): {path} ({size} bytes)"
            )
            self.large_files.append(path)

        # Duplicate name tracking
        self.duplicates[os.path.basename(path)].append(path)

        return {
            "path": path,
            "size": size,
            "extension": ext,
            "modified": modified,
        }

    # ------------------------------------------------------------------
    # COUNTER INTEGRITY CHECK
    # ------------------------------------------------------------------
    def _verify_counters(self) -> None:
        """Raise RuntimeError if counter invariant is violated."""
        if self.total_discovered != self.total_processed + self.total_failed:
            raise RuntimeError(
                f"Counter mismatch: discovered={self.total_discovered}, "
                f"processed={self.total_processed}, failed={self.total_failed}"
            )

    # ------------------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------------------
    def get_summary(self) -> Dict:
        """Return a serialisable summary dict. Verifies counters first."""
        self._verify_counters()
        return {
            "total_discovered": self.total_discovered,
            "total_processed": self.total_processed,
            "total_failed": self.total_failed,
            "extension_count": dict(self.extension_count),
            "large_files": list(self.large_files),
            "duplicates": dict(self.duplicates),
        }

    # ------------------------------------------------------------------
    # LOGGING HELPERS
    # ------------------------------------------------------------------
    def report_summary(self) -> None:
        logging.info(f"Discovered : {self.total_discovered}")
        logging.info(f"Processed  : {self.total_processed}")
        logging.info(f"Failed     : {self.total_failed}")
        for ext, count in self.extension_count.items():
            logging.info(f"  {ext} → {count} file(s)")
        logging.info(f"Large files: {len(self.large_files)}")

    def report_duplicates(self) -> None:
        for name, paths in self.duplicates.items():
            if len(paths) > 1:
                logging.info(f"Duplicate → {name}: {paths}")