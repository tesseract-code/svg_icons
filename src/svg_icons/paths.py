from pathlib import Path


def _find_project_root(start: Path, marker: str = ".project-root") -> Path:
    for parent in [start, *start.parents]:
        if (parent / marker).exists():
            return parent
    raise RuntimeError(f"Could not find '{marker}' above {start}")

# place .project-root at rooot directory
_PROJECT_ROOT = _find_project_root(Path(__file__))

LINE_ICONS = _PROJECT_ROOT / "svg_icons" / "src" / "svg_icons" / "line"
FILL_ICONS = _PROJECT_ROOT / "svg_icons" / "src" / "svg_icons" / "fill"
OTHER_ICONS = _PROJECT_ROOT / "svg_icons" / "src" / "svg_icons" / "other"
