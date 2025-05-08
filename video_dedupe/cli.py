import sys
from pathlib import Path
import click

from video_dedupe.database.db import init_db
from video_dedupe.dedupe import run as dedupe_run
from video_dedupe.organize import organize_canonical


@click.group()
def cli():
    """Video Deduplication & Organization Tool CLI"""
    pass


@cli.command("init")
def init_command():
    """Initialize the database schema (create tables)."""
    init_db()


@cli.command("dedupe")
@click.argument("root_dir", type=click.Path(exists=True, file_okay=False))
@click.option(
    "--ignore-dir", "ignore_dirs",
    multiple=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory to ignore (can be specified multiple times)."
)
def dedupe_command(root_dir, ignore_dirs):
    """
    Scan and dedupe videos under ROOT_DIR, skipping any IGNORE_DIR(s).
    """
    try:
        ignores = [Path(d) for d in ignore_dirs] if ignore_dirs else None
        dedupe_run(root_dir, ignores)
    except Exception as e:
        click.echo(f"❌ Error during dedupe: {e}")
        sys.exit(1)


@cli.command("organize")
@click.argument("dest_dir", type=click.Path(file_okay=False))
def organize_command(dest_dir):
    """
    Transfer all canonical videos into DEST_DIR via hard link → symlink → copy fallback.
    Reports any failures and exits with code 1 if any.
    """
    # Clean up whitespace or accidental newline chars in the path
    dest = dest_dir.strip()
    try:
        failures = organize_canonical(Path(dest))
        if failures:
            sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error during organize: {e}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error during organize: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
