"""
organize.py
Recursively sorts icons into fill/ or line/ subdirectories based on filename.

Usage:
    python organize_icons.py <icons_dir>
    python organize_icons.py <icons_dir> --dry-run
"""
from __future__ import annotations

import argparse
import logging
import shutil
import sys
from pathlib import Path

from pycore.log.ctx import ContextAdapter

logger = ContextAdapter(logging.getLogger(__name__), {})

_ICON_EXTENSIONS = {".svg", ".png", ".ico", ".icns", ".webp"}
_CATEGORIES = ("fill", "line")
_FALLBACK = "other"


def categorise(path: Path) -> str:
    """Return 'fill', 'line', or 'other'."""
    stem = path.stem.lower()
    for category in _CATEGORIES:
        if category in stem:
            return category
    return _FALLBACK


def organize(root: Path, dry_run: bool = False) -> None:
    moved = 0
    skipped = 0

    icons = [
        p for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in _ICON_EXTENSIONS
    ]

    for icon in icons:
        category = categorise(icon)
        dest_dir = root / category
        dest_path = dest_dir / icon.name

        if icon.parent.resolve() == dest_dir.resolve():
            skipped += 1
            continue

        if dest_path.exists():
            dest_path = dest_dir / f"{icon.stem}__{icon.parent.name}{icon.suffix}"

        logger.info(f"  [{'dry' if dry_run else 'mv'}] {icon.relative_to(root)}"
              f"  →  {dest_path.relative_to(root)}")

        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(icon), dest_path)

        moved += 1

    logger.info(f"\n{'[DRY RUN] ' if dry_run else ''}Done — "
          f"moved: {moved}, already sorted: {skipped}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("directory", type=Path,
                        help="Root directory to organise")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would happen without moving anything")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    if not args.directory.is_dir():
        logger.error(f"Error: '{args.directory}' is not a directory.",
                file=sys.stderr)
        sys.exit(1)

    logger.info(f"{'[DRY RUN] ' if args.dry_run else ''}Organising icons in: "
          f"{args.directory.resolve()}\n")

    organize(args.directory, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
