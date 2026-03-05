import os
from typing import Any, Dict


class ReportWriter:
    """Writes a scan summary as a formatted Markdown report."""

    def __init__(self, output_dir: str) -> None:
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def write_report(
        self, summary: Dict[str, Any], filename: str = "scan_report.md"
    ) -> str:
        """
        Write the scan summary to a Markdown file.

        Args:
            summary: Dict returned by FileScanner.get_summary().
            filename: Output filename (default: scan_report.md).

        Returns:
            Absolute path to the generated report file.
        """
        report_path = os.path.join(self.output_dir, filename)

        with open(report_path, "w", encoding="utf-8") as f:

            f.write("# File System Scan Report\n\n")

            # ── Scan Counters ────────────────────────────────────────
            f.write("## Scan Counters\n\n")
            f.write(f"- **Total Discovered**: {summary['total_discovered']}\n")
            f.write(f"- **Total Processed**:  {summary['total_processed']}\n")
            f.write(f"- **Total Failed**:     {summary['total_failed']}\n\n")

            # ── File Extensions ──────────────────────────────────────
            f.write("## File Extensions Count\n\n")
            if summary["extension_count"]:
                for ext, count in sorted(
                    summary["extension_count"].items(),
                    key=lambda x: x[1],
                    reverse=True,
                ):
                    f.write(f"- **{ext}**: {count}\n")
            else:
                f.write("_None found._\n")
            f.write("\n")

            # ── Large Files ──────────────────────────────────────────
            f.write("## Large Files\n\n")
            if summary["large_files"]:
                for path in summary["large_files"]:
                    f.write(f"- `{path}`\n")
            else:
                f.write("_None detected._\n")
            f.write("\n")

            # ── Duplicate File Names ─────────────────────────────────
            f.write("## Duplicate File Names\n\n")
            duplicates = {
                name: paths
                for name, paths in summary["duplicates"].items()
                if len(paths) > 1
            }
            if duplicates:
                for name, paths in duplicates.items():
                    f.write(f"### `{name}`\n")
                    for p in paths:
                        f.write(f"- `{p}`\n")
                    f.write("\n")
            else:
                f.write("_No duplicates found._\n")

        return report_path