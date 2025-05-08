import xxhash
import tempfile
from pathlib import Path
from video_dedupe.hashing import hash_file

def test_hash_empty(tmp_path):
    f = tmp_path / "empty.bin"
    f.write_bytes(b"")
    expected = xxhash.xxh64(b"").hexdigest()
    assert hash_file(f) == expected

def test_hash(tmp_path):
    content = b"hello world"
    f = tmp_path / "hello.bin"
    f.write_bytes(content)
    expected = xxhash.xxh64(content).hexdigest()
    assert hash_file(f) == expected
