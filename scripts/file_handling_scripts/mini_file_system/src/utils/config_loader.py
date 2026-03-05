import json
import logging
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

# Immutable reference — never mutate this directly.
# Use _get_default_config() to get a safe working copy.
_DEFAULT_CONFIG: Dict[str, Any] = {
    "target_folder": "data",
    "large_file_threshold_mb": 10,
    "log_level": "DEBUG",
}

_VALID_LOG_LEVELS = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"}


def _get_default_config() -> Dict[str, Any]:
    """Return a deep copy of the default configuration."""
    return deepcopy(_DEFAULT_CONFIG)


def load_config(config_path: str = "config/config.json") -> Dict[str, Any]:
    """
    Load configuration from a JSON file.

    - If the file does not exist, it is created with default values.
    - Values are validated and coerced to their expected types.
    - An invalid log_level falls back to 'INFO' with a warning.

    Args:
        config_path: Path to the JSON config file.

    Returns:
        Validated configuration dictionary.

    Raises:
        TypeError: If a required field has the wrong type and cannot be coerced.
    """
    cfg_path = Path(config_path)
    cfg_path.parent.mkdir(parents=True, exist_ok=True)

    if not cfg_path.exists():
        default = _get_default_config()
        cfg_path.write_text(json.dumps(default, indent=2), encoding="utf-8")
        logging.info(f"Config not found — created default at: {cfg_path}")
        config = default
    else:
        try:
            config = json.loads(cfg_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise ValueError(f"Config file is not valid JSON: {cfg_path}") from e

    # ── Validate: target_folder ──────────────────────────────────────
    if not isinstance(config.get("target_folder"), str):
        raise TypeError("config['target_folder'] must be a string")

    # ── Validate: large_file_threshold_mb ───────────────────────────
    try:
        config["large_file_threshold_mb"] = int(
            config.get("large_file_threshold_mb", 10)
        )
    except (TypeError, ValueError) as e:
        raise TypeError(
            "config['large_file_threshold_mb'] must be an integer"
        ) from e

    # ── Validate: log_level ──────────────────────────────────────────
    if not isinstance(config.get("log_level"), str):
        raise TypeError("config['log_level'] must be a string")

    config["log_level"] = config["log_level"].strip().upper()
    if config["log_level"] not in _VALID_LOG_LEVELS:
        logging.warning(
            f"Unsupported log_level '{config['log_level']}'. Falling back to 'INFO'."
        )
        config["log_level"] = "INFO"

    return config