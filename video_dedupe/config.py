import os
from dotenv import load_dotenv


load_dotenv()

DB_URL = os.getenv("DATABASE_URL") or (
    f"postgresql://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}"
    f"@{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
)

VIDEO_EXTS = {
    ".3g2",
    ".3gp",
    ".3gpp",
    ".amv",
    ".asf",
    ".avi",
    ".bik",
    ".divx",
    ".drc",
    ".dv",
    ".f4v",
    ".flv",
    ".h264",
    ".m1v",
    ".m2p",
    ".m2ts",
    ".m2v",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp2",
    ".mp2v",
    ".mp4",
    ".mpe",
    ".mpeg",
    ".mpg",
    ".mpv",
    ".mts",
    ".nsv",
    ".ogg",
    ".ogm",
    ".ogv",
    ".qt",
    ".rm",
    ".rmvb",
    ".roq",
    ".smk",
    ".svi",
    ".vob",
    ".vro",
    ".webm",
    ".wm",
    ".wmv",
    ".wtv",
    ".yuv",
    ".mod",
    ".ts",
    ".xvid",
    ".rv",
    ".viv"
}