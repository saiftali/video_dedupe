import xxhash

from pathlib import Path


def hash_file(path: Path) -> str:
    hashing_function = xxhash.xxh64()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): # 1 << 20 = 1MB
            hashing_function.update(chunk)
    return hashing_function.hexdigest()