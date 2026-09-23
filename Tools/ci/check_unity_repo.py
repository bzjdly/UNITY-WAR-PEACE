#!/usr/bin/env python3
"""Validate repository boundaries and Unity asset hygiene."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAX_REGULAR_FILE_BYTES = 5 * 1024 * 1024
GENERATED_ROOT_DIRS = {
    ".gradle",
    ".idea",
    ".vs",
    "build",
    "builds",
    "library",
    "logs",
    "memorycaptures",
    "obj",
    "recordings",
    "temp",
    "usersettings",
}
LFS_BINARY_EXTENSIONS = {
    ".3ds",
    ".7z",
    ".a",
    ".aac",
    ".aar",
    ".abc",
    ".aif",
    ".aiff",
    ".blend",
    ".bmp",
    ".bundle",
    ".dae",
    ".dll",
    ".dylib",
    ".exr",
    ".fbx",
    ".flac",
    ".gif",
    ".hdr",
    ".jpeg",
    ".jpg",
    ".m4a",
    ".ma",
    ".max",
    ".mb",
    ".mov",
    ".mp3",
    ".mp4",
    ".obj",
    ".ogg",
    ".otf",
    ".pdf",
    ".png",
    ".psb",
    ".psd",
    ".rar",
    ".so",
    ".stl",
    ".tga",
    ".tif",
    ".tiff",
    ".ttf",
    ".unitypackage",
    ".wav",
    ".webm",
    ".zip",
}
TEXT_SUFFIXES = {
    ".asset",
    ".asmdef",
    ".asmref",
    ".cs",
    ".json",
    ".md",
    ".meta",
    ".txt",
    ".unity",
    ".yaml",
    ".yml",
}
REQUIRED_PATHS = {
    ".gitattributes",
    ".gitignore",
    "Packages/manifest.json",
    "Packages/packages-lock.json",
    "ProjectSettings/ProjectVersion.txt",
}


def git(*args: str) -> bytes:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        stderr=subprocess.PIPE,
    )


def tracked_files() -> list[str]:
    output = git("ls-files", "-z")
    return sorted(
        item.decode("utf-8", errors="surrogateescape")
        for item in output.split(b"\0")
        if item
    )


def filter_attribute(path: str) -> str:
    output = git("check-attr", "filter", "--", path).decode(
        "utf-8", errors="replace"
    )
    return output.rsplit(": ", 1)[-1].strip()


def add_meta_errors(paths: list[str], tracked: set[str]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        if not path.startswith("Assets/"):
            continue

        if path.endswith(".meta"):
            asset_path = path.removesuffix(".meta")
            if asset_path in tracked or (ROOT / asset_path).is_dir():
                continue
            errors.append(f"orphan Unity meta file: {path}")
        elif f"{path}.meta" not in tracked:
            errors.append(f"missing Unity meta file: {path}.meta")
    return errors


def add_lfs_errors(paths: list[str]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        file_path = ROOT / path
        suffix = file_path.suffix.lower()
        requires_lfs = suffix in LFS_BINARY_EXTENSIONS

        if file_path.is_file() and file_path.stat().st_size > MAX_REGULAR_FILE_BYTES:
            requires_lfs = True

        if requires_lfs and filter_attribute(path) != "lfs":
            errors.append(f"binary or large file is not managed by Git LFS: {path}")
    return errors


def add_conflict_marker_errors(paths: list[str]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        file_path = ROOT / path
        if file_path.suffix.lower() not in TEXT_SUFFIXES or not file_path.is_file():
            continue

        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        if any(
            marker in content
            for marker in ("<<<<<<< ", "=======\n", ">>>>>>> ")
        ):
            errors.append(f"unresolved merge conflict marker: {path}")
    return errors


def main() -> int:
    try:
        git("rev-parse", "--is-inside-work-tree")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: run this check inside a Git working tree.", file=sys.stderr)
        return 1

    paths = tracked_files()
    tracked = set(paths)
    errors: list[str] = []

    for required_path in sorted(REQUIRED_PATHS - tracked):
        errors.append(f"required file is not tracked: {required_path}")

    ignored = git("ls-files", "-ci", "--exclude-standard").decode(
        "utf-8", errors="replace"
    )
    for path in ignored.splitlines():
        errors.append(f"ignored generated file is tracked: {path}")

    for path in paths:
        root = path.split("/", 1)[0].lower()
        if root in GENERATED_ROOT_DIRS:
            errors.append(f"generated directory is tracked: {path}")

    errors.extend(add_meta_errors(paths, tracked))
    errors.extend(add_lfs_errors(paths))
    errors.extend(add_conflict_marker_errors(paths))

    if errors:
        print("Repository validation failed:")
        for error in dict.fromkeys(errors):
            print(f"  - {error}")
        return 1

    print(f"Repository validation passed for {len(paths)} tracked files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
