import numpy as np

from src.face_data import block_mean, identity_split
from src.face_study import reconstruct
from src.projectors import grid_laplacian


def test_face_partitions_cover_each_identity_and_are_disjoint():
    splits = identity_split(20261117)
    np.testing.assert_array_equal(np.sort(np.concatenate(splits)), np.arange(400))
    for rows, count, replay in zip(splits, (6, 2, 2), identity_split(20261117), strict=True):
        np.testing.assert_array_equal(np.bincount(rows // 10), np.full(40, count))
        np.testing.assert_array_equal(rows, replay)


def test_box_average_preserves_constants_and_orientation():
    x = np.arange(24.0).reshape(1, 4, 6)
    reduced = block_mean(x, (2, 3))
    np.testing.assert_array_equal(reduced[0], [[3.5, 5.5, 7.5], [15.5, 17.5, 19.5]])
    np.testing.assert_array_equal(block_mean(np.full((2, 64, 64), .5), (16, 16)),
                                  np.full((2, 16, 16), .5))
    laplacian = grid_laplacian((2, 3))
    assert laplacian[2, 3] == 0


def test_nonorthogonal_reconstruction_matches_independent_least_squares():
    w = np.array([[1., 1.], [0., 2.], [1., 0.], [0., 1.]])
    mean = np.array([2., 0., 1., 3.])
    x = np.array([[1., 2., 3., 4.], [3., -1., 2., 1.]])
    coef = np.linalg.lstsq(w, (x-mean).T, rcond=None)[0]
    predicted = reconstruct(x, mean, w)
    np.testing.assert_allclose(predicted, mean + (w @ coef).T, atol=1e-13)
    np.testing.assert_allclose(reconstruct(predicted, mean, w), predicted, atol=1e-13)
    np.testing.assert_allclose((x-predicted) @ w, 0, atol=1e-13)
