"""Load selected Olivetti rows and reduce the source grid by fixed block averaging."""
from pathlib import Path
from urllib.request import urlretrieve

import numpy as np
from scipy.io import loadmat

from src.data import file_hash

SOURCE_URL = "https://ndownloader.figshare.com/files/5976027"
SOURCE_SHA = "b612fb967f2dc77c9c62d3e1266e0c73d5fca46a4b8906c18e454d41af987794"
FILENAME = "olivettifaces.mat"
IDENTITIES = 40
IMAGES_PER_IDENTITY = 10


def fetch_faces(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / FILENAME
    if not path.exists():
        partial = path.with_suffix(".part")
        urlretrieve(SOURCE_URL, partial)
        if file_hash(partial) != SOURCE_SHA:
            raise ValueError("Downloaded Olivetti checksum does not match")
        partial.replace(path)
    return path


def identity_split(seed):
    """Assign six fit, two validation and two test images per identity."""
    rng = np.random.default_rng(seed)
    blocks = np.stack([
        rng.permutation(np.arange(i, i + IMAGES_PER_IDENTITY))
        for i in range(0, IDENTITIES * IMAGES_PER_IDENTITY, IMAGES_PER_IDENTITY)
    ])
    return tuple(np.sort(blocks[:, sl].ravel()) for sl in (slice(0, 6), slice(6, 8),
                                                        slice(8, 10)))


def block_mean(images, shape):
    """Integer-factor box filter then decimate along both spatial axes."""
    n, height, width = images.shape
    rows, cols = shape
    if rows < 1 or cols < 1 or height % rows or width % cols:
        raise ValueError("Output dimensions must divide the source dimensions")
    return images.reshape(n, rows, height // rows, cols, width // cols).mean(axis=(2, 4))


def load_faces(directory, indices, shape):
    """Read only selected rows into the image analysis arrays after archive decoding."""
    path = Path(directory) / FILENAME
    if file_hash(path) != SOURCE_SHA:
        raise ValueError("Olivetti source file differs from the documented release")
    raw = loadmat(path, variable_names=["faces"])["faces"]
    if raw.shape != (4096, IDENTITIES * IMAGES_PER_IDENTITY):
        raise ValueError("Unexpected Olivetti archive dimensions")
    selected = raw[:, indices].T
    if not np.isfinite(selected).all() or selected.min() < 0 or selected.max() > 255:
        raise ValueError("Unexpected grayscale values")
    # The source vectors are column-major. Match scikit-learn's orientation.
    images = selected.reshape(len(indices), 64, 64).transpose(0, 2, 1) / 255
    reduced = block_mean(images, shape)
    return np.ascontiguousarray(reduced.reshape(len(indices), -1)), indices // IMAGES_PER_IDENTITY
