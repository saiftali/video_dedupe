import os
import shutil
from pathlib import Path
from video_dedupe.database.db import get_conn


def organize_canonical(dest_dir: Path):
    """Organize canonical files into DEST_DIR."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    failures = []

    sql = "SELECT path FROM files WHERE dedupe_stage = 'canonical';"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql)

    for (path_str,) in cur.fetchall():
        src = Path(path_str)
        dst = dest_dir / src.name
        try:
            # Attempt hard link
            if dst.exists() or dst.is_symlink():
                dst.unlink()
            os.link(src, dst)
        except Exception as e1:
            try:
                # Fallback to symbolic link
                if dst.exists() or dst.is_symlink():
                    dst.unlink()
                os.symlink(src, dst)
            except Exception as e2:
                try:
                    # Fallback to copy
                    shutil.copy2(src, dst)
                except Exception as e3:
                    failures.append((src, f"hardlink failed: {e1}; symlink failed: {e2}; copy failed: {e3}"))
    cur.close()
    conn.close()

    # Report failures
    if failures:
        print("Some files failed to transfer:")
        for src, err in failures:
            print(f" - {src}: {err}")
    else:
        print("✅ All canonical files transferred successfully.")

    return failures
