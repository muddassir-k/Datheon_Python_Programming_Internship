#!/usr/bin/env python3
"""Sort files in a directory into extension-based category folders."""

import argparse
import os
import shutil
from pathlib import Path


EXTENSION_CATEGORIES = {
    ".doc": "Documents",
    ".docx": "Documents",
    ".odt": "Documents",
    ".pdf": "Documents",
    ".rtf": "Documents",
    ".txt": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".tif": "Images",
    ".tiff": "Images",
    ".svg": "Images",
    ".webp": "Images",
    ".mp4": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",
    ".mkv": "Videos",
    ".wmv": "Videos",
    ".flv": "Videos",
    ".webm": "Videos",
    ".mp3": "Videos",
    ".wav": "Videos",
    ".aac": "Videos",
    ".flac": "Videos",
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".bz2": "Archives",
    ".xz": "Archives",
    ".py": "Code",
    ".js": "Code",
    ".ts": "Code",
    ".jsx": "Code",
    ".tsx": "Code",
    ".html": "Code",
    ".css": "Code",
    ".java": "Code",
    ".c": "Code",
    ".h": "Code",
    ".cpp": "Code",
    ".cs": "Code",
    ".go": "Code",
    ".rs": "Code",
    ".php": "Code",
    ".rb": "Code",
    ".sh": "Code",
    ".sql": "Code",
}


def available_destination(directory: Path, filename: str) -> Path:
    """Return a destination path that does not currently exist."""
    candidate = directory / filename
    if not candidate.exists():
        return candidate

    source = Path(filename)
    suffix = "".join(source.suffixes)
    stem = filename[: -len(suffix)] if suffix else filename
    number = 1
    while True:
        candidate = directory / f"{stem} ({number}){suffix}"
        if not candidate.exists():
            return candidate
        number += 1


def organize(directory: Path) -> tuple[int, int, int]:
    """Move recognized files; return (moved, skipped, failed) counts."""
    moved = skipped = failed = 0

    try:
        entries = list(os.scandir(directory))
    except (PermissionError, OSError) as error:
        print(f"Cannot access {directory}: {error}")
        return moved, skipped, failed + 1

    for entry in entries:
        try:
            if not entry.is_file(follow_symlinks=False):
                continue
            category = EXTENSION_CATEGORIES.get(Path(entry.name).suffix.lower())
            if category is None:
                skipped += 1
                continue

            target_directory = directory / category
            target_directory.mkdir(exist_ok=True)
            destination = available_destination(target_directory, entry.name)

            # Retry a collision if another process creates the destination meanwhile.
            while True:
                try:
                    shutil.move(entry.path, destination)
                    moved += 1
                    break
                except FileExistsError:
                    destination = available_destination(target_directory, entry.name)
        except (PermissionError, OSError) as error:
            print(f"Could not move {entry.name}: {error}")
            failed += 1

    return moved, skipped, failed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Organize files into Documents, Images, Videos, Archives, and Code."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=Path.home() / "Downloads",
        help="directory to organize (default: ~/Downloads)",
    )
    args = parser.parse_args()

    if not args.directory.is_dir():
        parser.error(f"not a directory: {args.directory}")

    moved, skipped, failed = organize(args.directory)
    print("\nOrganization complete")
    print(f"  Files relocated: {moved}")
    print(f"  Unrecognized files skipped: {skipped}")
    print(f"  Failures: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
