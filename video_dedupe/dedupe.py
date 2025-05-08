from pathlib import Path
from typing import List, Tuple
from video_dedupe.scanner import scan_videos
from video_dedupe.hashing import hash_file
from video_dedupe.database.db import upsert_files

def run(root_dir: str, ignore_dirs: List[str] = None) -> None:
    root = Path(root_dir)
    hash_groups: dict[str, List[Tuple[Path, float]]] = {}

    count = 0
    for path in scan_videos(root, ignore_dirs):
        count += 1
        if count % 100 == 0:
            print(f"[{count}] Hashing {path.name}…")
        mtime = path.stat().st_mtime
        hval  = hash_file(path)
        hash_groups.setdefault(hval, []).append((path, mtime))


    #INSERT
    records: List[Tuple[str, float, None, str, str]] = []
    for hval, items in hash_groups.items():
        # first item is canonical
        canon_path, canon_mtime = items[0]
        records.append((str(canon_path), canon_mtime, None, hval, "canonical"))
        # the rest are duplicates
        for dup_path, dup_mtime in items[1:]:
            records.append((str(dup_path), dup_mtime, None, hval, "duplicate"))
    upsert_files(records)
    
    
    total_files = sum(len(v) for v in hash_groups.values())
    dupes = total_files - len(hash_groups)
    print(f"✅ Dedupe run complete: {len(hash_groups)} uniques, {dupes} duplicates found.")