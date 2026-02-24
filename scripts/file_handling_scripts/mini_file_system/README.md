# 📁 Mini File System Scanner — Complete Beginner's Guide

> **Who is this for?** Complete beginners. Every single keyword, every function, every line of code is explained in simple English. No assumptions. Baby steps only.

---

## 🗺️ Table of Contents

1. [What Does This Project Do?](#what-does-this-project-do)
2. [Project Structure](#project-structure)
3. [How All Scripts Connect](#how-all-scripts-connect)
4. [Script 1 — path_manager.py](#script-1--path_managerpy)
5. [Script 2 — file_scanner.py](#script-2--file_scannerpy)
6. [Script 3 — main.py](#script-3--mainpy)
7. [Script 4 — report_writer.py](#script-4--report_writerpy)
8. [Complete Call Flow](#complete-call-flow)
9. [Common Errors & Fixes](#common-errors--fixes)
10. [Python Keywords Glossary](#python-keywords-glossary)
11. [How to Run](#how-to-run)

---

## What Does This Project Do?

Imagine you have a hard drive with **thousands of files** scattered across hundreds of folders. This project is a smart robot that:

```
1. Walks into every folder and subfolder (like a postman checking every house)
2. Reads info about every file — size, type, last modified date
3. Flags files bigger than your threshold (e.g. files > 10 MB)
4. Spots duplicate filenames (same name appearing in different folders)
5. Writes a clean Markdown report (.md file) with all findings
```

**4 scripts = 4 workers. Each has one job. `main.py` is the boss.**

---

## Project Structure

```
mini_file_system/
├── config/
│   └── config.json          ← settings file (auto-created if missing)
├── data/
│   └── your_files_here/     ← the folder that gets scanned
├── logs/
│   └── app.log              ← all log messages saved here
├── src/
│   ├── reports/
│   │   └── scan_report.md   ← the final output report
│   ├── utils/
│   │   ├── path_manager.py  ← Script 1: finds & validates paths
│   │   ├── file_scanner.py  ← Script 2: scans files & collects data
│   │   ├── config_loader.py ← loads and validates config.json
│   │   └── report_writer.py ← Script 4: writes the .md report
│   └── main.py              ← Script 3: the boss, runs everything
```

---

## How All Scripts Connect

```
You run: python -m src.main
              │
              ▼
         ┌─────────┐
         │ main.py │  ← The Director. Calls everyone else.
         └────┬────┘
              │
    ┌─────────┼──────────────┐
    ▼         ▼              ▼
┌───────────┐  ┌──────────────┐  ┌───────────────┐
│config_    │  │path_manager  │  │file_scanner   │
│loader.py  │  │.py           │  │.py            │
│           │  │              │  │               │
│Reads      │  │Resolves &    │  │Walks folders, │
│config.json│  │validates     │  │reads file     │
│Returns    │  │file paths    │  │metadata       │
│settings   │  │              │  │               │
└───────────┘  └──────────────┘  └───────┬───────┘
                                          │
                                          ▼
                                 ┌─────────────────┐
                                 │ report_writer.py│
                                 │                 │
                                 │ Takes summary   │
                                 │ dict, writes    │
                                 │ scan_report.md  │
                                 └─────────────────┘
```

---

---

# Script 1 — `path_manager.py`

> **Job:** Your GPS for the file system. Give it a short name like `"data"` and it gives back the full path like `D:\project\mini_file_system\data`.

---

## The Full Code

```python
from pathlib import Path                                    # Line 1


class PathManager:                                          # Line 4
    @staticmethod                                           # Line 5
    def resolve_path(base_path: str | Path, relative_path: str) -> str:   # Line 6
        return str((Path(base_path) / relative_path).resolve())            # Line 7

    @staticmethod                                           # Line 9
    def ensure_exists(                                      # Line 10
        path: str | Path,                                   # Line 11
        expected_type: str = "file",                        # Line 12
        create_if_missing: bool = False,                    # Line 13
    ) -> bool:                                              # Line 14
        p = Path(path)                                      # Line 15

        if expected_type == "dir":                          # Line 17
            if not p.is_dir():                              # Line 18
                if create_if_missing:                       # Line 19
                    p.mkdir(parents=True, exist_ok=True)    # Line 20
                else:                                       # Line 21
                    raise NotADirectoryError(f"Directory not found: {p}")  # Line 22
            return True                                     # Line 23

        if expected_type == "file":                         # Line 25
            if not p.is_file():                             # Line 26
                raise FileNotFoundError(f"File not found: {p}")            # Line 27
            return True                                     # Line 28

        raise ValueError("expected_type must be 'file' or 'dir'")         # Line 30
```

---

## Line-by-Line Explanation

### Line 1 — `from pathlib import Path`

```python
from pathlib import Path
```

**What it means:** Import (borrow) the `Path` tool from Python's built-in `pathlib` library.

- `pathlib` = a Python library that makes working with file paths easy
- `Path` = the main class inside pathlib that represents a file/folder path
- Without this, we'd have to manually join paths with strings — messy and error-prone on different operating systems

**Real-world analogy:** Like importing a GPS tool into your car. Without it you'd have to manually calculate directions.

```python
# Without pathlib (old messy way):
full_path = base + "\\" + folder + "\\" + file   # breaks on Mac/Linux!

# With pathlib (clean way):
full_path = Path(base) / folder / file           # works everywhere ✓
```

---

### Line 4 — `class PathManager:`

```python
class PathManager:
```

**What it means:** Create a container called `PathManager` that holds related functions together.

- `class` = keyword that defines a blueprint/container
- `PathManager` = the name we give this container
- Think of a class like a toolbox — all path-related tools live inside it
- We never create an object from it (`pm = PathManager()`) — we call it directly

```python
# How we USE this class (from main.py):
PathManager.resolve_path(PROJECT_ROOT, "data")
PathManager.ensure_exists(target_folder, expected_type="dir")
```

---

### Line 5 — `@staticmethod`

```python
@staticmethod
```

**What it means:** A decorator that marks the function below as "static".

- `@` = this is a decorator (modifies the function below it)
- `staticmethod` = this function belongs to the CLASS, not to any specific object
- Normally to use a class function you'd write: `pm = PathManager()` then `pm.resolve_path(...)` 
- With `@staticmethod` you skip the object creation: `PathManager.resolve_path(...)` directly
- That's why there's NO `self` parameter in these functions

---

### Line 6 — `def resolve_path(base_path: str | Path, relative_path: str) -> str:`

```python
def resolve_path(base_path: str | Path, relative_path: str) -> str:
```

Breaking this down piece by piece:

| Part | Meaning |
|------|---------|
| `def` | Define a new function |
| `resolve_path` | The function's name |
| `base_path: str \| Path` | Parameter that can be a `str` OR a `Path` object — the `\|` means OR |
| `relative_path: str` | Parameter that must be a string |
| `-> str` | This function will RETURN a string |

**Type hints** (`: str`, `-> str`) are just documentation for developers — Python doesn't enforce them. They tell you what to expect going in and coming out.

---

### Line 7 — `return str((Path(base_path) / relative_path).resolve())`

```python
return str((Path(base_path) / relative_path).resolve())
```

This one line does 4 things. Let's peel it apart:

```python
# Step 1: Wrap base_path in a Path object
Path(base_path)
# "D:/project/mini_file_system" → Path("D:/project/mini_file_system")

# Step 2: Use / operator to join paths (pathlib magic!)
Path(base_path) / relative_path
# Path("D:/project/mini_file_system") / "data"
# = Path("D:/project/mini_file_system/data")

# Step 3: .resolve() converts to absolute path (fixes ../ and ./ etc)
(...).resolve()
# = Path("D:\\project\\mini_file_system\\data")

# Step 4: str() converts Path object back to a plain string
str(...)
# = "D:\\project\\mini_file_system\\data"
```

The `/` operator between two `Path` objects joins them. This is pathlib's clever design — much cleaner than string concatenation.

---

### Line 12 — `expected_type: str = "file"`

```python
expected_type: str = "file",
```

**What it means:** A parameter with a **default value**.

- If the caller doesn't pass `expected_type`, it automatically uses `"file"`
- `= "file"` is the default value

```python
# These are all valid calls:
ensure_exists(path)                          # uses default: "file"
ensure_exists(path, expected_type="dir")     # overrides to "dir"
ensure_exists(path, "dir", True)             # positional arguments
```

---

### Line 15 — `p = Path(path)`

```python
p = Path(path)
```

**What it means:** Wrap the incoming `path` string inside a `Path` object so we can use Path methods on it.

- `path` arrives as a plain string: `"D:/project/data"`
- We wrap it: `p = Path("D:/project/data")`  
- Now `p` has useful methods: `p.is_dir()`, `p.is_file()`, `p.mkdir()`
- Without wrapping, we'd just have a plain string with no file-system methods

---

### Line 18 — `if not p.is_dir():`

```python
if not p.is_dir():
```

- `p.is_dir()` = checks if this path is an existing folder on disk. Returns `True` or `False`
- `not` = flips the result. `not True` = `False`, `not False` = `True`
- So this reads: **"if the folder does NOT exist..."**

---

### Line 20 — `p.mkdir(parents=True, exist_ok=True)`

```python
p.mkdir(parents=True, exist_ok=True)
```

**Creates the folder on disk.** Two important arguments:

| Argument | Meaning |
|----------|---------|
| `parents=True` | Also create any missing parent folders. Like `mkdir -p` in terminal. |
| `exist_ok=True` | Don't crash if folder already exists. Without this, it would throw an error. |

```python
# Example:
p = Path("D:/project/reports/monthly/jan")
p.mkdir(parents=True, exist_ok=True)
# Creates: D:/project/reports/   ← parent
#          D:/project/reports/monthly/  ← parent
#          D:/project/reports/monthly/jan/  ← target
```

---

### Line 22 — `raise NotADirectoryError(f"Directory not found: {p}")`

```python
raise NotADirectoryError(f"Directory not found: {p}")
```

- `raise` = deliberately throw an error to stop execution
- `NotADirectoryError` = a built-in Python error type for missing directories
- `f"Directory not found: {p}"` = f-string: the `{p}` is replaced with the actual path value
- This gives the caller a clear, helpful error message instead of a cryptic crash

---

## Function Summary — path_manager.py

### `resolve_path(base_path, relative_path)` → `str`

**Purpose:** Joins two path pieces and returns the full absolute path.

```
Called by:  main.py
Input:      base_path = PROJECT_ROOT, relative_path = "data"
Output:     "D:\\project\\mini_file_system\\data"
```

**Decision flow:**
```
base_path + relative_path
        ↓
   Path object joined with /
        ↓
   .resolve() makes it absolute
        ↓
   str() converts to string
        ↓
   returned to main.py
```

---

### `ensure_exists(path, expected_type, create_if_missing)` → `bool`

**Purpose:** Verifies a path exists. Creates it or throws an error if not.

```
Called by:  main.py
Input:      path = full folder path, expected_type = "dir", create_if_missing = True
Output:     True (if exists/created) or raises an error
```

**Decision flow:**
```
expected_type == "dir"?
    ├── YES: p.is_dir()?
    │       ├── YES → return True ✓
    │       └── NO  → create_if_missing?
    │               ├── YES → p.mkdir() → return True ✓
    │               └── NO  → raise NotADirectoryError ✗
    │
    └── NO: expected_type == "file"?
            ├── YES: p.is_file()?
            │       ├── YES → return True ✓
            │       └── NO  → raise FileNotFoundError ✗
            └── NO → raise ValueError ✗
```

---

---

# Script 2 — `file_scanner.py`

> **Job:** The detective. Walks into every folder and subfolder, reads information about every file, and tracks statistics.

**Real-world analogy:** A census worker who visits every house in a city, writes down number of rooms, when it was built, size — for every single house.

---

## The Full Code

```python
import os                                                   # Line 1
import logging                                              # Line 2
from collections import defaultdict                         # Line 3
from typing import Dict, Generator, Optional               # Line 4
from datetime import datetime                               # Line 5


class FileScanner:                                          # Line 8
    def __init__(self, root_path: str,                      # Line 9
                 large_file_threshold_mb: int = 10) -> None:
        self.root_path = root_path                          # Line 11
        self.large_file_threshold_bytes = large_file_threshold_mb * 1024 * 1024  # Line 12

        self.total_discovered: int = 0                      # Line 15
        self.total_processed: int  = 0                      # Line 16
        self.total_failed: int     = 0                      # Line 17

        self.extension_count = defaultdict(int)             # Line 19
        self.large_files     = []                           # Line 20
        self.duplicates      = defaultdict(list)            # Line 21

    def scan(self) -> Generator[Optional[Dict], None, None]:   # Line 23
        for root, _, files in os.walk(self.root_path):         # Line 24
            for filename in files:                             # Line 25
                full_path = os.path.join(root, filename)       # Line 26
                self.total_discovered += 1                     # Line 27

                try:                                           # Line 29
                    meta = self._extract_metadata(full_path)   # Line 30
                    self.total_processed += 1                  # Line 31
                    yield meta                                  # Line 32

                except Exception as e:                         # Line 34
                    self.total_failed += 1                     # Line 35
                    logging.error(f"[FAILED] {full_path} → {e}")  # Line 36
                    yield None                                  # Line 37

        self._verify_counters()                                # Line 39

    def _extract_metadata(self, path: str) -> Dict:            # Line 41
        if "fail" in os.path.basename(path).lower():           # Line 42
            raise RuntimeError("Simulated failure")            # Line 43

        size     = os.path.getsize(path)                       # Line 45
        ext      = os.path.splitext(path)[1] or "<no-ext>"    # Line 46
        modified = datetime.fromtimestamp(                     # Line 47
            os.path.getmtime(path)
        ).strftime("%Y-%m-%d %H:%M:%S")

        self.extension_count[ext] += 1                         # Line 51

        if size == 0:                                          # Line 53
            logging.warning(f"Zero-byte file: {path}")        # Line 54
        elif size > self.large_file_threshold_bytes:           # Line 55
            self.large_files.append(path)                      # Line 56
            logging.warning(f"Large file: {path}")            # Line 57

        self.duplicates[os.path.basename(path)].append(path)  # Line 59

        return {                                               # Line 61
            "path":      path,
            "size":      size,
            "extension": ext,
            "modified":  modified,
        }

    def _verify_counters(self) -> None:                        # Line 68
        if self.total_discovered != self.total_processed + self.total_failed:
            raise RuntimeError(
                f"Counter mismatch: discovered={self.total_discovered}, "
                f"processed={self.total_processed}, failed={self.total_failed}"
            )

    def get_summary(self) -> Dict:                             # Line 75
        self._verify_counters()
        return {
            "total_discovered": self.total_discovered,
            "total_processed":  self.total_processed,
            "total_failed":     self.total_failed,
            "extension_count":  dict(self.extension_count),
            "large_files":      list(self.large_files),
            "duplicates":       dict(self.duplicates),
        }

    def report_summary(self) -> None:                          # Line 86
        logging.info(f"Discovered : {self.total_discovered}")
        logging.info(f"Processed  : {self.total_processed}")
        logging.info(f"Failed     : {self.total_failed}")
        for ext, count in self.extension_count.items():
            logging.info(f"  {ext} → {count} file(s)")

    def report_duplicates(self) -> None:                       # Line 93
        for name, paths in self.duplicates.items():
            if len(paths) > 1:
                logging.info(f"Duplicate → {name}: {paths}")
```

---

## Imports Explained (Lines 1–5)

```python
import os
```
Python's built-in `os` module. Gives us tools to talk to the Operating System:
- `os.walk()` — walk through folder trees
- `os.path.join()` — safely combine path pieces
- `os.path.getsize()` — get file size in bytes
- `os.path.getmtime()` — get last-modified timestamp
- `os.path.basename()` — extract just the filename from a full path

---

```python
import logging
```
Python's built-in logging module. Better than `print()` because:
- Writes to both terminal AND a log file simultaneously
- Has levels: `DEBUG` < `INFO` < `WARNING` < `ERROR` < `CRITICAL`
- You can filter — e.g. only show `WARNING` and above
- Each message gets a timestamp automatically

```python
# Different levels:
logging.debug("Tiny detail")       # only in DEBUG mode
logging.info("Normal message")     # general info
logging.warning("Watch out!")      # something unusual
logging.error("Something failed!") # an error occurred
```

---

```python
from collections import defaultdict
```
A special dictionary that **auto-creates a default value** when you access a missing key.

```python
# Normal dict — crashes on missing key:
normal = {}
normal["txt"] += 1   # KeyError! "txt" doesn't exist yet

# defaultdict(int) — starts from 0 automatically:
counts = defaultdict(int)
counts["txt"] += 1   # works! Starts at 0, becomes 1 ✓

# defaultdict(list) — starts from [] automatically:
groups = defaultdict(list)
groups["file.txt"].append("/path1")  # works! Starts as [], adds path ✓
```

---

```python
from typing import Dict, Generator, Optional
```
Type hints — documentation for developers, not enforced by Python.

| Type | Meaning |
|------|---------|
| `Dict` | A dictionary (key-value pairs) |
| `Generator` | A function that `yield`s values one at a time |
| `Optional` | The value can be this type OR `None` |

---

```python
from datetime import datetime
```
The `datetime` class for working with dates and times. We use it to convert a raw Unix timestamp number (like `1705320720`) into a readable string like `"2024-01-15 14:32:00"`.

---

## `__init__` — The Setup (Lines 9–21)

```python
def __init__(self, root_path: str, large_file_threshold_mb: int = 10) -> None:
```

`__init__` is Python's **constructor** — it runs automatically the moment you create an object:

```python
# This line in main.py:
scanner = FileScanner(target_folder, threshold_mb)
#                     ↑              ↑
#                 root_path    large_file_threshold_mb

# Automatically calls __init__ which sets up:
self.root_path = target_folder
self.large_file_threshold_bytes = threshold_mb * 1024 * 1024
self.total_discovered = 0
self.total_processed  = 0
self.total_failed     = 0
self.extension_count  = defaultdict(int)
self.large_files      = []
self.duplicates       = defaultdict(list)
```

**What is `self`?**

`self` refers to the current object instance. Every instance of FileScanner has its OWN copy of these variables.

```python
scanner_A = FileScanner("/folder_A")   # has its own counters
scanner_B = FileScanner("/folder_B")   # has its own separate counters
# scanner_A.total_discovered ≠ scanner_B.total_discovered
```

**`* 1024 * 1024` — MB to bytes conversion:**
```
1 MB = 1024 KB
1 KB = 1024 bytes
∴ 1 MB = 1024 × 1024 = 1,048,576 bytes
∴ 10 MB = 10 × 1,048,576 = 10,485,760 bytes
```

---

## `scan()` — The Main Loop (Lines 23–39)

```python
def scan(self) -> Generator[Optional[Dict], None, None]:
```

**Return type breakdown:** `Generator[Optional[Dict], None, None]`
- This is a **Generator function** — it uses `yield` to produce values one at a time
- `Optional[Dict]` = each yielded value is either a `Dict` or `None`
- Memory efficient: processes one file at a time, never loads everything into RAM

---

### `os.walk(self.root_path)` — The Magic Iterator

```python
for root, _, files in os.walk(self.root_path):
```

`os.walk()` is the heart of the scanner. It visits every folder recursively:

```
Folder structure:
data/
├── notes.txt
├── images/
│   ├── photo.jpg
│   └── logo.png
└── docs/
    └── report.pdf

os.walk("data/") gives us 3 iterations:
  Iteration 1: root="data/",        dirs=["images","docs"], files=["notes.txt"]
  Iteration 2: root="data/images/", dirs=[],                files=["photo.jpg","logo.png"]
  Iteration 3: root="data/docs/",   dirs=[],                files=["report.pdf"]
```

The `_` variable holds the subdirectory names — we don't need them (os.walk handles recursion itself), so we use `_` as a convention meaning "I'm ignoring this value".

---

### `os.path.join(root, filename)` — Building the Full Path

```python
full_path = os.path.join(root, filename)
```

```
root     = "D:/data/images"
filename = "photo.jpg"
result   = "D:/data/images/photo.jpg"
```

Why not just `root + "/" + filename`? Because:
- On Windows the separator is `\`, on Mac/Linux it's `/`
- `os.path.join()` handles this automatically — it uses the correct separator for the OS

---

### `try / except` — Error Handling

```python
try:
    meta = self._extract_metadata(full_path)
    self.total_processed += 1
    yield meta

except Exception as e:
    self.total_failed += 1
    logging.error(f"[FAILED] {full_path} → {e}")
    yield None
```

**What is `try/except`?**

```
try block:
    Run this code.
    If ANY error happens → immediately jump to except block.
    If no error → continue normally.

except block:
    An error happened. Handle it here.
    The program does NOT crash.
```

**Why do we need it here?**
- Files can be locked by another program
- We might not have permission to read a file
- The file could be deleted between `os.walk` finding it and us reading it
- Without `try/except`, one bad file crashes the ENTIRE scan

**`except Exception as e:`**
- `Exception` is the base class of ALL Python errors
- `as e` stores the error object in variable `e` so we can log what went wrong

**`yield None` on failure:**
- We explicitly yield `None` to tell the caller "this file failed"
- The caller checks `if meta is not None:` to skip failed files
- This way the caller always knows how many files were attempted

---

### `yield` vs `return` — Key Difference

```python
# return — function ends, gives ONE value back:
def get_all_files():
    result = []
    for file in all_files:
        result.append(process(file))
    return result   # waits until ALL done, uses lots of memory

# yield — function pauses, gives ONE value at a time:
def scan():
    for file in all_files:
        yield process(file)   # gives result immediately, pauses, continues
```

`yield` is perfect here because:
- `main.py` gets each file's metadata immediately (doesn't wait for all files)
- If there are 1 million files, we never hold 1 million dicts in memory at once

---

## `_extract_metadata()` — Reading File Details (Lines 41–65)

```python
def _extract_metadata(self, path: str) -> Dict:
```

The underscore prefix `_` in `_extract_metadata` is a Python convention meaning **"private method"** — it's meant to be called only from within this class, not from outside.

---

### Line-by-Line Inside `_extract_metadata`

```python
if "fail" in os.path.basename(path).lower():
    raise RuntimeError("Simulated failure")
```
- `os.path.basename(path)` — extracts just the filename: `"D:/data/fail_test.txt"` → `"fail_test.txt"`
- `.lower()` — converts to lowercase so `"FAIL"`, `"Fail"`, `"fail"` all match
- `"fail" in ...` — checks if `"fail"` appears anywhere in the filename
- If yes: `raise RuntimeError(...)` — deliberately crash this file (for testing)

---

```python
size = os.path.getsize(path)
```
Returns the file size in **bytes** as an integer. Example: `10485760` = 10 MB.

---

```python
ext = os.path.splitext(path)[1] or "<no-ext>"
```

`os.path.splitext()` splits a filename into `(name, extension)`:

```python
os.path.splitext("report.txt")    → ("report", ".txt")
os.path.splitext("archive.tar.gz") → ("archive.tar", ".gz")
os.path.splitext("Makefile")      → ("Makefile", "")
```

- `[1]` gets the second element (the extension part)
- `or "<no-ext>"` — if extension is `""` (empty string, which is falsy), use `"<no-ext>"` instead
- The `or` keyword returns the right side when the left side is falsy

---

```python
modified = datetime.fromtimestamp(
    os.path.getmtime(path)
).strftime("%Y-%m-%d %H:%M:%S")
```

Step by step:

```python
os.path.getmtime(path)
# → 1705320720.0   (Unix timestamp: seconds since Jan 1, 1970)

datetime.fromtimestamp(1705320720.0)
# → datetime(2024, 1, 15, 14, 32, 0)   (datetime object)

.strftime("%Y-%m-%d %H:%M:%S")
# → "2024-01-15 14:32:00"   (readable string)

# Format codes:
# %Y = 4-digit year (2024)
# %m = 2-digit month (01)
# %d = 2-digit day (15)
# %H = 2-digit hour 24h (14)
# %M = 2-digit minute (32)
# %S = 2-digit second (00)
```

---

```python
self.extension_count[ext] += 1
```

Thanks to `defaultdict(int)`, this works even the first time we see an extension:

```python
# First time we see ".txt":
# defaultdict auto-creates: extension_count[".txt"] = 0
# Then: extension_count[".txt"] = 0 + 1 = 1

# Second time we see ".txt":
# extension_count[".txt"] = 1 + 1 = 2
```

---

```python
if size == 0:
    logging.warning(f"Zero-byte file: {path}")
elif size > self.large_file_threshold_bytes:
    self.large_files.append(path)
    logging.warning(f"Large file: {path}")
```

- `if size == 0` — empty file, just warn
- `elif` = "else if" — only checked if the first condition was False
- `size > self.large_file_threshold_bytes` — file is bigger than our limit (default 10MB)
- `.append(path)` — add this path to the end of the `large_files` list

---

```python
self.duplicates[os.path.basename(path)].append(path)
```

Tracks every filename and where it appears:

```python
# If we see these files:
# D:/data/notes.txt
# D:/data/archive/notes.txt
# D:/data/backup/notes.txt

# duplicates becomes:
{
    "notes.txt": [
        "D:/data/notes.txt",
        "D:/data/archive/notes.txt",
        "D:/data/backup/notes.txt"
    ]
}
```

Later, `report_duplicates()` checks `if len(paths) > 1` — only THOSE are true duplicates.

---

```python
return {
    "path":      path,
    "size":      size,
    "extension": ext,
    "modified":  modified,
}
```

Return a **dictionary** (key-value pairs) with all the file's metadata. This dict is what gets `yield`ed back to `main.py`.

---

## `_verify_counters()` — Safety Check (Lines 68–73)

```python
def _verify_counters(self) -> None:
    if self.total_discovered != self.total_processed + self.total_failed:
        raise RuntimeError(
            f"Counter mismatch: discovered={self.total_discovered}, "
            f"processed={self.total_processed}, failed={self.total_failed}"
        )
```

**The math invariant:** Every file we see (`discovered`) must either succeed (`processed`) OR fail (`failed`). Nothing can disappear.

```
discovered = processed + failed  ← must ALWAYS be true
```

> ⚠️ **Why `RuntimeError` and NOT `assert`?**
>
> `assert` is **disabled** when Python runs with the `-O` (optimize) flag:
> ```bash
> python -O src/main.py   # assert statements are SKIPPED!
> ```
> `RuntimeError` **always** runs regardless of flags. Production code must use `RuntimeError`, never `assert` for critical checks.

---

## `get_summary()` — Package the Results (Lines 75–84)

```python
def get_summary(self) -> Dict:
    self._verify_counters()
    return {
        "total_discovered": self.total_discovered,
        "total_processed":  self.total_processed,
        "total_failed":     self.total_failed,
        "extension_count":  dict(self.extension_count),
        "large_files":      list(self.large_files),
        "duplicates":       dict(self.duplicates),
    }
```

- `dict(self.extension_count)` — converts `defaultdict` to a plain `dict`. Callers don't need defaultdict's special behaviour
- `list(self.large_files)` — returns a **copy** of the list. If caller modifies it, our internal list is safe
- This dict is passed directly to `ReportWriter.write_report()`

---

---

# Script 3 — `main.py`

> **Job:** The director. Doesn't scan files itself, doesn't write reports itself — but tells every other script WHEN to do WHAT and passes data between them.

**Real-world analogy:** A film director. They don't act, don't do makeup, don't handle lighting — but they coordinate everyone and call "action" at the right time.

---

## The Full Code

```python
import os                                                   # Line 1
import logging                                              # Line 2
import argparse                                             # Line 3
from pathlib import Path                                    # Line 4

from src.utils.path_manager   import PathManager            # Line 6
from src.utils.file_scanner   import FileScanner            # Line 7
from src.utils.config_loader  import load_config            # Line 8
from src.utils.report_writer  import ReportWriter           # Line 9

# Module-level constant — computed ONCE when file loads     # Line 11
PROJECT_ROOT = Path(__file__).resolve().parent.parent       # Line 12


def setup_logging(level_str: str) -> None:                  # Line 15
    log_dir = PROJECT_ROOT / "logs"                         # Line 16
    log_dir.mkdir(parents=True, exist_ok=True)              # Line 17

    level = getattr(logging, level_str.upper(), logging.DEBUG)  # Line 19

    logging.basicConfig(                                    # Line 21
        level=level,
        format="%(asctime)s — %(levelname)s — %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "app.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def parse_args() -> argparse.Namespace:                     # Line 30
    parser = argparse.ArgumentParser(description="Mini File System Scanner")
    parser.add_argument("--folder",       type=str, help="Override target folder")
    parser.add_argument("--threshold_mb", type=int, help="Override large-file MB")
    parser.add_argument("--report",       type=str, default="scan_report.md")
    return parser.parse_args()


def main() -> None:                                         # Line 37
    config = load_config(str(PROJECT_ROOT / "config" / "config.json"))  # Step 1

    setup_logging(config["log_level"])                      # Step 2

    args = parse_args()                                     # Step 3
    target_folder_name = args.folder or config["target_folder"]
    threshold_mb       = args.threshold_mb or config["large_file_threshold_mb"]

    target_folder = PathManager.resolve_path(PROJECT_ROOT, target_folder_name)  # Step 4

    logging.debug(f"Project root : {PROJECT_ROOT}")
    logging.debug(f"CWD          : {os.getcwd()}")
    logging.debug(f"Target folder: {target_folder}")

    PathManager.ensure_exists(target_folder, expected_type="dir",  # Step 5
                               create_if_missing=True)

    scanner = FileScanner(target_folder, threshold_mb)      # Step 6

    for meta in scanner.scan():                             # Step 7
        if meta is not None:
            logging.info(meta)

    scanner.report_duplicates()                             # Step 8
    scanner.report_summary()

    scan_summary = scanner.get_summary()                    # Step 9

    reports_dir = str(PROJECT_ROOT / "reports")
    writer   = ReportWriter(reports_dir)                    # Step 10
    out_path = writer.write_report(scan_summary, filename=args.report)

    logging.info(f"Report saved : {out_path}")              # Step 11


if __name__ == "__main__":                                  # Line 68
    main()
```

---

## Line-by-Line Explanation

### Lines 6–9 — Importing From Our Own Scripts

```python
from src.utils.path_manager  import PathManager
from src.utils.file_scanner  import FileScanner
from src.utils.config_loader import load_config
from src.utils.report_writer import ReportWriter
```

These import our own scripts. The format is `from <folder.subfolder.filename> import <ClassName>`.

```
src/
└── utils/
    ├── path_manager.py   → PathManager class
    ├── file_scanner.py   → FileScanner class
    ├── config_loader.py  → load_config function
    └── report_writer.py  → ReportWriter class
```

Python finds these because we run with `python -m src.main` from the `mini_file_system/` folder, making Python aware of the `src` package.

---

### Line 12 — `PROJECT_ROOT` — The Most Important Line

```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent
```

This is defined **outside any function** (module level). It runs once when the file loads and is shared by all functions.

Step by step:

```
__file__
  = "D:/ai_lab/mini_file_system/src/main.py"
  (Python automatically sets __file__ to the current script's path)

Path(__file__)
  = Path("D:/ai_lab/mini_file_system/src/main.py")

.resolve()
  = Path("D:/ai_lab/mini_file_system/src/main.py")
  (makes it absolute — resolves any ../ or ./ in the path)

.parent
  = Path("D:/ai_lab/mini_file_system/src/")
  (go up one level — from main.py to its containing folder: src/)

.parent  (second time)
  = Path("D:/ai_lab/mini_file_system/")
  (go up one more level — from src/ to mini_file_system/)

← THIS is PROJECT_ROOT ✓
```

**Why two `.parent`?**
Because `main.py` lives inside `src/`. One `.parent` gets us to `src/`. Two `.parent` gets us to `mini_file_system/` (the project root where `config/`, `data/`, `logs/`, `reports/` live).

**Why module-level and not inside `main()`?**
Because `setup_logging()` also needs it. Defining it once at module level means all functions share the exact same value — no inconsistency possible.

---

### `setup_logging()` — Lines 15–28

```python
def setup_logging(level_str: str) -> None:
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
```

**`getattr(logging, level_str.upper(), logging.DEBUG)`**

This is a clever trick to convert a string like `"DEBUG"` into the actual `logging.DEBUG` constant:

```python
# The long way:
if level_str == "DEBUG":
    level = logging.DEBUG
elif level_str == "INFO":
    level = logging.INFO
# ... etc

# getattr short way:
level = getattr(logging, "DEBUG", logging.DEBUG)
# getattr(object, attribute_name, default)
# = logging.DEBUG   ← same as typing logging.DEBUG directly!

# If level_str is invalid (e.g. "BANANA"), uses default: logging.DEBUG
```

**`level_str.upper()`** — converts `"debug"` → `"DEBUG"`. Config might store lowercase, `logging` needs uppercase.

**Two handlers simultaneously:**
```python
handlers=[
    logging.FileHandler(log_dir / "app.log", encoding="utf-8"),  # → writes to file
    logging.StreamHandler(),                                        # → writes to terminal
]
```
Every `logging.info()` call goes to BOTH places at the same time.

**Format string breakdown:**
```
"%(asctime)s — %(levelname)s — %(message)s"
        ↑               ↑              ↑
   timestamp       DEBUG/INFO/etc   your message

Example output:
"2024-01-15 14:32:00,123 — INFO — Scanning complete"
```

---

### `parse_args()` — Lines 30–35

```python
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mini File System Scanner")
    parser.add_argument("--folder",       type=str, help="Override target folder")
    parser.add_argument("--threshold_mb", type=int, help="Override large-file MB")
    parser.add_argument("--report",       type=str, default="scan_report.md")
    return parser.parse_args()
```

`argparse` lets users pass options from the terminal:

```bash
# No arguments — uses config.json defaults:
python -m src.main

# Override folder:
python -m src.main --folder my_data_folder

# Override threshold to 5 MB:
python -m src.main --threshold_mb 5

# Custom report filename:
python -m src.main --report june_report.md

# All combined:
python -m src.main --folder data --threshold_mb 5 --report june.md
```

`parser.parse_args()` reads whatever was typed in the terminal and returns a `Namespace` object. Access values like: `args.folder`, `args.threshold_mb`, `args.report`.

---

### `main()` — The Orchestrator

```python
target_folder_name = args.folder or config["target_folder"]
```

**Python `or` short-circuit logic:**

```python
# args.folder is None if user didn't pass --folder
# None is "falsy" in Python
# So:
None or "data"      → "data"      (uses config)
"mydir" or "data"   → "mydir"     (uses CLI argument)
```

CLI arguments always override config when provided.

---

```python
for meta in scanner.scan():
    if meta is not None:
        logging.info(meta)
```

**Why `is not None` and not just `if meta`?**

```python
# These are DIFFERENT:
if meta:           # False for: None, {}, [], 0, ""  ← WRONG if meta could be empty dict
if meta is not None:  # False ONLY for None  ← CORRECT
```

Because `meta` could theoretically be an empty `{}` dict for some edge case, we use the explicit `is not None` check. This is the correct, safe way to check for `None` specifically.

---

### Line 68 — `if __name__ == "__main__":`

```python
if __name__ == "__main__":
    main()
```

**This is the entry point guard.** Every Python script has a built-in variable `__name__`.

```python
# When you RUN a file directly (python -m src.main):
__name__ == "__main__"   ← True → main() gets called ✓

# When another file IMPORTS this file:
__name__ == "src.main"   ← NOT "__main__" → main() does NOT run ✓
```

Without this guard, if any other script ever did `import main`, the entire scan would run automatically — a nasty surprise. This guard prevents that.

---

---

# Script 4 — `report_writer.py`

> **Job:** The publisher. Takes the raw statistics dictionary from FileScanner and writes it into a clean, formatted Markdown `.md` file.

**Real-world analogy:** A journalist who takes interview notes (raw data) and writes a clean, readable newspaper article.

---

## The Full Code

```python
import os                                                   # Line 1
from typing import Dict, Any                               # Line 2


class ReportWriter:                                         # Line 5
    def __init__(self, output_dir: str) -> None:            # Line 6
        self.output_dir = output_dir                        # Line 7
        os.makedirs(self.output_dir, exist_ok=True)         # Line 8

    def write_report(                                       # Line 10
        self,
        summary: Dict[str, Any],
        filename: str = "scan_report.md"
    ) -> str:
        report_path = os.path.join(self.output_dir, filename)  # Line 15

        with open(report_path, "w", encoding="utf-8") as f:    # Line 17

            # ── Section 1: Title ──────────────────────────────
            f.write("# File System Scan Report\n\n")            # Line 20

            # ── Section 2: Counters ───────────────────────────
            f.write("## Scan Counters\n\n")                     # Line 23
            f.write(f"- **Total Discovered**: {summary['total_discovered']}\n")
            f.write(f"- **Total Processed**:  {summary['total_processed']}\n")
            f.write(f"- **Total Failed**:     {summary['total_failed']}\n\n")

            # ── Section 3: Extensions ─────────────────────────
            f.write("## File Extensions Count\n\n")             # Line 29
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

            # ── Section 4: Large Files ────────────────────────
            f.write("## Large Files\n\n")                       # Line 41
            if summary["large_files"]:
                for path in summary["large_files"]:
                    f.write(f"- `{path}`\n")
            else:
                f.write("_None detected._\n")
            f.write("\n")

            # ── Section 5: Duplicates ─────────────────────────
            f.write("## Duplicate File Names\n\n")              # Line 50
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

        return report_path                                  # Line 65
```

---

## Line-by-Line Explanation

### Line 2 — `from typing import Dict, Any`

```python
from typing import Dict, Any
```

- `Dict` = dictionary type hint
- `Any` = the value can be anything — `int`, `str`, `list`, `dict`, etc.
- `Dict[str, Any]` = "a dictionary where keys are strings and values can be any type"

The `summary` dict coming from `get_summary()` has mixed value types (ints, lists, dicts), so `Any` is correct here.

---

### Line 8 — `os.makedirs(self.output_dir, exist_ok=True)`

```python
os.makedirs(self.output_dir, exist_ok=True)
```

Called in `__init__` so the output folder is created **before** we try to write anything. If we waited until `write_report()`, we'd get a `FileNotFoundError` trying to write to a non-existent folder.

---

### Line 17 — `with open(report_path, "w", encoding="utf-8") as f:`

```python
with open(report_path, "w", encoding="utf-8") as f:
```

This is the **context manager** pattern. Breaking it down:

| Part | Meaning |
|------|---------|
| `open(report_path, ...)` | Open the file at `report_path` |
| `"w"` | Write mode — creates the file if it doesn't exist, **overwrites** if it does |
| `encoding="utf-8"` | Use UTF-8 encoding — supports all characters worldwide |
| `as f` | Give the opened file the name `f` so we can write to it |
| `with ...` | Context manager — guarantees file is closed when block ends |

**Why `with`?** Without `with`, if an error occurs mid-write, the file stays open and gets corrupted. `with` guarantees `f.close()` is always called — even if an exception occurs.

```python
# Without with (dangerous):
f = open("report.md", "w")
f.write("data...")      # if error here, file never gets closed!
f.close()               # might never run

# With with (safe):
with open("report.md", "w") as f:
    f.write("data...")  # if error here, file still gets closed ✓
```

**`"w"` vs `"a"` mode:**

```
"w" = Write mode:  starts fresh, overwrites existing content
"a" = Append mode: adds to end of existing content
"r" = Read mode:   only reads, can't write
```

---

### Lines 31–36 — `sorted()` with `lambda`

```python
for ext, count in sorted(
    summary["extension_count"].items(),
    key=lambda x: x[1],
    reverse=True,
):
```

**`dict.items()`** — loops over a dictionary giving both key AND value:

```python
{"txt": 15, "py": 8, "md": 3}.items()
# gives: [(".txt", 15), (".py", 8), (".md", 3)]
#         ↑ tuple of (key, value)
```

**`sorted(..., key=lambda x: x[1], reverse=True)`** — sort by count, highest first:

```python
# lambda is a tiny anonymous function:
lambda x: x[1]
# = "given any x, return x[1]"
# For tuple (".txt", 15):   x[1] = 15
# For tuple (".py",  8):    x[1] = 8

# So sorted() compares the counts and orders by them
# reverse=True = biggest count first

# Result order: .txt(15), .py(8), .md(3)
```

**Why not just `def`?** A `lambda` is for tiny one-line functions that you only need in one place. It's shorter than writing a full `def` function.

---

### Lines 50–62 — Dictionary Comprehension for Duplicates

```python
duplicates = {
    name: paths
    for name, paths in summary["duplicates"].items()
    if len(paths) > 1
}
```

This is a **dictionary comprehension** — builds a new dict in one expression:

```python
# Long way (same result):
duplicates = {}
for name, paths in summary["duplicates"].items():
    if len(paths) > 1:
        duplicates[name] = paths

# Short way (dictionary comprehension):
duplicates = {name: paths for name, paths in summary["duplicates"].items() if len(paths) > 1}
```

The `if len(paths) > 1` filter means we ONLY include filenames that appear in 2+ locations — those are true duplicates. Files that appear only once are excluded.

---

### Line 65 — `return report_path`

```python
return report_path
```

Returns the full path of the created report file so `main.py` can log:
```
INFO — Report saved: D:/project/mini_file_system/reports/scan_report.md
```

---

## What the Generated Report Looks Like

```markdown
# File System Scan Report

## Scan Counters

- **Total Discovered**: 42
- **Total Processed**:  40
- **Total Failed**:     2

## File Extensions Count

- **.py**: 15
- **.txt**: 12
- **.md**: 8
- **<no-ext>**: 5

## Large Files

- `D:/project/data/bigarchive.zip`

## Duplicate File Names

### `README.md`
- `D:/project/docs/README.md`
- `D:/project/src/README.md`

### `config.json`
- `D:/project/config/config.json`
- `D:/project/backup/config.json`
```

---

---

# Complete Call Flow

This is exactly what happens, step by step, when you run `python -m src.main`:

```
Step  1  │ Terminal          │ You type: python -m src.main
Step  2  │ Python            │ Loads main.py, computes PROJECT_ROOT = mini_file_system/
Step  3  │ main()            │ Calls load_config("mini_file_system/config/config.json")
Step  4  │ load_config()     │ Reads config.json → validates → returns settings dict
Step  5  │ main()            │ Calls setup_logging("DEBUG")
Step  6  │ setup_logging()   │ Creates logs/ folder, configures logging to file+terminal
Step  7  │ main()            │ Calls parse_args() → reads any --folder / --threshold_mb
Step  8  │ main()            │ Resolves: target_folder_name = args.folder OR config value
Step  9  │ main()            │ Calls PathManager.resolve_path(PROJECT_ROOT, "data")
Step 10  │ resolve_path()    │ Joins paths → returns "D:/project/mini_file_system/data"
Step 11  │ main()            │ Calls PathManager.ensure_exists(target_folder, "dir", True)
Step 12  │ ensure_exists()   │ Checks folder exists, creates it if not → returns True
Step 13  │ main()            │ Creates: scanner = FileScanner(target_folder, threshold_mb)
Step 14  │ FileScanner.__init__ │ Sets up all counters and empty data structures
Step 15  │ main()            │ Starts loop: for meta in scanner.scan()
Step 16  │ scan()            │ os.walk() finds first folder, gets list of files
Step 17  │ scan()            │ Calls _extract_metadata(full_path) for each file
Step 18  │ _extract_metadata │ Reads size, ext, date → updates counters → returns Dict
Step 19  │ scan()            │ yield meta → sends Dict to main() loop
Step 20  │ main()            │ if meta is not None: logs the metadata dict
Step 21  │ [repeats 16-20]   │ For every single file in every subfolder
Step 22  │ scan()            │ All files done → calls _verify_counters()
Step 23  │ _verify_counters()│ Checks discovered == processed + failed
Step 24  │ main()            │ Calls scanner.report_duplicates() → logs duplicate names
Step 25  │ main()            │ Calls scanner.report_summary() → logs final counts
Step 26  │ main()            │ Calls scanner.get_summary() → gets full stats dict
Step 27  │ main()            │ Creates: writer = ReportWriter("mini_file_system/reports/")
Step 28  │ ReportWriter.__init__ │ Creates reports/ folder if it doesn't exist
Step 29  │ main()            │ Calls writer.write_report(scan_summary, "scan_report.md")
Step 30  │ write_report()    │ Opens file, writes all 5 sections, closes file
Step 31  │ write_report()    │ Returns report path string to main()
Step 32  │ main()            │ logging.info("Report saved: ...") → DONE ✓
```

---

---

# Common Errors & Fixes

| Error | Why it happens | How to fix |
|-------|---------------|------------|
| `FileNotFoundError` | Path doesn't exist and `create_if_missing=False` | Check your `config.json` — is `target_folder` set to `"data"`? |
| `NotADirectoryError` | You expected a folder but it doesn't exist | Make sure `data/` folder exists at project root level |
| `RuntimeError: Counter mismatch` | `_verify_counters()` failed — a bug in the code | A file was discovered but never counted as processed or failed |
| `ModuleNotFoundError: src.utils...` | Python can't find our scripts | Run from `mini_file_system/` folder: `cd mini_file_system` then `python -m src.main` |
| `json.JSONDecodeError` | `config.json` has bad syntax | Check for missing commas, brackets, or quotes in config.json |
| `PermissionError` | No permission to read a file or create a folder | Run terminal as administrator, or check folder permissions |
| `TypeError: config[...] must be...` | Wrong type in config.json | `target_folder` needs quotes `"data"`, `large_file_threshold_mb` needs no quotes: `10` |
| `UnicodeDecodeError` | Binary file or non-UTF-8 file encountered | The `try/except` in `scan()` handles this — check the log for `[FAILED]` entries |

---

---

# Python Keywords Glossary

| Keyword | Simple Explanation | Example |
|---------|-------------------|---------|
| `import` | Borrow a library so you can use its tools | `import os` |
| `from X import Y` | Borrow only one specific thing from a library | `from pathlib import Path` |
| `class` | Define a container/blueprint that holds related functions | `class FileScanner:` |
| `def` | Define a reusable block of code with a name | `def scan(self):` |
| `self` | Inside a class, refers to the current object instance | `self.root_path = root_path` |
| `return` | Send a value back to whoever called the function, then stop | `return report_path` |
| `yield` | Like return, but the function PAUSES and can continue later | `yield meta` |
| `try` | Attempt to run code that might fail | `try: meta = extract(path)` |
| `except` | What to do if the try block throws an error | `except Exception as e:` |
| `raise` | Deliberately throw an error with a custom message | `raise ValueError("bad input")` |
| `if` | Only run code if a condition is True | `if size > threshold:` |
| `elif` | "Else if" — another condition to check if the first was False | `elif size == 0:` |
| `else` | Run this if ALL conditions above were False | `else: return True` |
| `for` | Loop over every item in a collection | `for file in files:` |
| `in` | Check if something is inside a collection | `"fail" in filename` |
| `not` | Flip True to False and False to True | `if not p.is_dir():` |
| `or` | Return left side if it's truthy, otherwise right side | `args.folder or config["folder"]` |
| `and` | Both sides must be True | `if x > 0 and x < 10:` |
| `is not None` | Check if a variable is specifically NOT None | `if meta is not None:` |
| `+=` | Shortcut for adding to a variable | `count += 1` same as `count = count + 1` |
| `@staticmethod` | This function can be called without creating an object | `@staticmethod def resolve_path(...)` |
| `lambda` | A tiny one-line anonymous function | `lambda x: x[1]` |
| `with` | Opens something and guarantees it gets closed | `with open(path) as f:` |
| `f"..."` | f-string: embed variable values directly in text | `f"Found {count} files"` |
| `dict` | A collection of key-value pairs | `{"size": 1024, "ext": ".txt"}` |
| `list` | An ordered collection of items | `["file1.txt", "file2.py"]` |
| `defaultdict` | A dict that auto-creates default values for new keys | `defaultdict(int)` |
| `__init__` | Constructor — runs automatically when creating an object | `def __init__(self, path):` |
| `__file__` | Built-in variable containing the current script's path | `Path(__file__).parent` |
| `__name__` | Built-in variable: `"__main__"` when run directly | `if __name__ == "__main__":` |
| `None` | Python's "nothing" value — means empty, missing, or not set | `yield None` |
| `True / False` | Boolean values — the result of comparisons | `p.is_dir()` returns `True` or `False` |

---

---

# How to Run

### Prerequisites

```bash
# Make sure you're in the project root folder:
cd D:/ai_engineering_lab/level_00_foundations/mini_file_system

# Activate virtual environment:
.venv\Scripts\activate    # Windows
source .venv/bin/activate  # Mac/Linux
```

### Basic Run

```bash
python -m src.main
```

### With Options

```bash
# Scan a different folder:
python -m src.main --folder my_custom_folder

# Change large file threshold to 5 MB:
python -m src.main --threshold_mb 5

# Save report with a custom name:
python -m src.main --report june_scan.md

# All options at once:
python -m src.main --folder data --threshold_mb 5 --report custom.md
```

### What to Expect

```
2024-01-15 14:32:00 — DEBUG — Project root : D:\...\mini_file_system
2024-01-15 14:32:00 — DEBUG — Target folder: D:\...\mini_file_system\data
2024-01-15 14:32:01 — INFO  — {'path': 'D:\\...\\data\\file.txt', 'size': 1024, ...}
2024-01-15 14:32:01 — INFO  — Discovered : 42
2024-01-15 14:32:01 — INFO  — Processed  : 40
2024-01-15 14:32:01 — INFO  — Failed     : 2
2024-01-15 14:32:01 — INFO  — Report saved: D:\...\mini_file_system\reports\scan_report.md
```

### Config File (`config/config.json`)

Auto-created on first run with these defaults:

```json
{
  "target_folder": "data",
  "large_file_threshold_mb": 10,
  "log_level": "DEBUG"
}
```

| Setting | What it does | Default |
|---------|-------------|---------|
| `target_folder` | Which folder to scan (relative to project root) | `"data"` |
| `large_file_threshold_mb` | Files bigger than this are flagged as large | `10` |
| `log_level` | How much detail to log (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | `"DEBUG"` |

---

*Made for beginners. Every keyword explained. No assumptions.* 🐣
