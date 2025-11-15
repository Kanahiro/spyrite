"""Tests for sprite generation script."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT_DIR / "main.py"
PADDING = 2


def _run_script(tmp_path: Path) -> tuple[Path, Path]:
    """Execute main.py inside tmp_path and return sprite & metadata paths."""

    subprocess.run([sys.executable, str(SCRIPT_PATH)], cwd=tmp_path, check=True)
    sprite_path = tmp_path / "sprite.png"
    meta_path = tmp_path / "sprite.json"
    return sprite_path, meta_path


def _make_icon(
    directory: Path, name: str, size: tuple[int, int], color: tuple[int, int, int, int]
) -> None:
    img = Image.new("RGBA", size, color)
    img.save(directory / f"{name}.png", format="PNG")


def test_creates_minimal_sprite_when_no_icons(tmp_path):
    """Running without icons should still create a blank sprite and empty metadata."""

    (tmp_path / "icons").mkdir()

    sprite_path, meta_path = _run_script(tmp_path)

    sprite = Image.open(sprite_path)
    assert sprite.size == (1, 1)

    with meta_path.open() as f:
        assert json.load(f) == {}


def test_creates_sprite_and_metadata_for_multiple_icons(tmp_path):
    icons_dir = tmp_path / "icons"
    icons_dir.mkdir()

    icon_specs = [
        ("pin", (4, 6), (255, 0, 0, 255)),
        ("shadow", (3, 4), (0, 0, 0, 128)),
        ("marker", (5, 2), (0, 255, 0, 255)),
    ]

    for name, size, color in icon_specs:
        _make_icon(icons_dir, name, size, color)

    sprite_path, meta_path = _run_script(tmp_path)

    sprite = Image.open(sprite_path)
    expected_width = sum(size[0] + PADDING for _, size, _ in icon_specs)
    expected_height = max(size[1] for _, size, _ in icon_specs)
    assert sprite.size == (expected_width, expected_height)

    with meta_path.open() as f:
        metadata = json.load(f)

    assert set(metadata.keys()) == {name for name, *_ in icon_specs}

    x_offset = 0
    for name, size, _ in icon_specs:
        entry = metadata[name]
        assert entry["x"] == x_offset
        assert entry["y"] == 0
        assert entry["width"] == size[0]
        assert entry["height"] == size[1]
        assert entry["pixelRatio"] == 1
        x_offset += size[0] + PADDING
