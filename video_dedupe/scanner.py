import os
from pathlib import Path
from typing import Iterator, Union
from video_dedupe.config import VIDEO_EXTS


def scan_videos(root: Path, ignore_dirs: Union[None, list[Path]] = None) -> Iterator[Path]:
    ignores = set()
    if ignore_dirs:
        for d in ignore_dirs:
            ignores.add(Path(d).resolve())

    for entry in os.scandir(root):
        entry_path = Path(entry.path)
        if any(entry_path.resolve().is_relative_to(ig) for ig in ignores):
            continue
        if entry.is_dir(follow_symlinks=False):
            yield from scan_videos(entry_path, ignore_dirs)
        elif entry.is_file(follow_symlinks=False) and entry_path.suffix.lower() in VIDEO_EXTS:
            yield entry_path
