from pathlib import Path


class PathManager:
    """Utility class for resolving and validating file system paths."""

    @staticmethod
    def resolve_path(base_path: str | Path, relative_path: str) -> str:
        """Resolve a relative path against a base path and return absolute string."""
        return str((Path(base_path) / relative_path).resolve())

    @staticmethod
    def ensure_exists(
        path: str | Path,
        expected_type: str = "file",
        create_if_missing: bool = False,
    ) -> bool:
        """
        Verify that a path exists and matches the expected type.

        Args:
            path: The file system path to check.
            expected_type: Either 'file' or 'dir'.
            create_if_missing: If True and expected_type is 'dir', create it.

        Returns:
            True if the path exists and matches the expected type.

        Raises:
            NotADirectoryError: If expected_type is 'dir' and path is not a directory.
            FileNotFoundError: If expected_type is 'file' and path is not a file.
            ValueError: If expected_type is not 'file' or 'dir'.
        """
        p = Path(path)

        if expected_type == "dir":
            if not p.is_dir():
                if create_if_missing:
                    p.mkdir(parents=True, exist_ok=True)
                else:
                    raise NotADirectoryError(f"Directory not found: {p}")
            return True

        if expected_type == "file":
            if not p.is_file():
                raise FileNotFoundError(f"File not found: {p}")
            return True

        raise ValueError("expected_type must be 'file' or 'dir'")