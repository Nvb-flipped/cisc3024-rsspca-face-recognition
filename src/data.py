"""Official partition loading and deterministic paired corruption."""
import hashlib
from pathlib import Path
from urllib.request import urlretrieve

import numpy as np

BASE_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/optdigits"
N_ROWS = {"tra": 3823, "tes": 1797}
TRAIN_SHA = "e1b683cc211604fe8fd8c4417e6a69f31380e0c61d4af22e93cc21e9257ffedd"


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fetch_partition(directory, suffix):
    if suffix not in N_ROWS:
        raise ValueError("Partition must be tra or tes")
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"optdigits.{suffix}"
    if not path.exists():
        temporary = path.with_suffix(f".{suffix}.part")
        urlretrieve(f"{BASE_URL}/{path.name}", temporary)
        temporary.replace(path)
    return path


def load_partition(directory, suffix):
    if suffix not in N_ROWS:
        raise ValueError("Partition must be tra or tes")
    path = Path(directory) / f"optdigits.{suffix}"
    digest = file_hash(path)
    if suffix == "tra" and digest != TRAIN_SHA:
        raise ValueError("Training hash differs from the official file observed at the gate")
    array = np.loadtxt(path, delimiter=",", dtype=np.int32)
    if array.shape != (N_ROWS[suffix], 65):
        raise ValueError(f"Unexpected shape in {path.name}")
    pixels, y = array[:, :-1], array[:, -1]
    if pixels.min() < 0 or pixels.max() > 16 or not np.array_equal(np.unique(y), np.arange(10)):
        raise ValueError(f"Invalid values in {path.name}")
    return pixels / 16.0, y, digest


def apply_masks(images, rows, locations, patches, shape, size):
    """Apply serialized corruption masks to a copy, keeping labels outside this function."""
    noisy = images.copy().reshape((-1, *shape))
    indices = np.arange(size)
    top, left = locations.T
    noisy[rows[:, None, None], top[:, None, None] + indices[:, None],
          left[:, None, None] + indices] = patches
    return noisy.reshape(images.shape)


def corrupt(images, fraction, seed, shape, size):
    """Generate the full mask sequence first so lower fractions use identical prefixes."""
    rng = np.random.default_rng(seed)
    height, width = shape
    count = int(fraction * len(images))
    rows = rng.permutation(len(images))[:count]
    locations = rng.integers([height - size + 1, width - size + 1], size=(len(images), 2))[:count]
    patches = rng.integers(0, 2, size=(len(images), size, size), dtype=np.uint8)[:count]
    return apply_masks(images, rows, locations, patches, shape, size), rows, locations, patches


def overlap(train, test):
    """Count exact feature collisions and contradictory labels in official partitions."""
    development = {}
    for x, y in zip(*train, strict=True):
        development.setdefault(x.tobytes(), set()).add(int(y))
    test_unique = {x.tobytes() for x in test[0]}
    cross = [(development[x.tobytes()], int(y)) for x, y in zip(*test, strict=True)
             if x.tobytes() in development]
    return {
        "development_unique": len(development),
        "development_conflicting_vectors": sum(len(labels) > 1 for labels in development.values()),
        "test_unique": len(test_unique),
        "cross_partition_matching_test_rows": len(cross),
        "cross_partition_conflicting_test_rows": sum(y not in labels for labels, y in cross),
    }
