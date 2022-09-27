"""Numpy related utils."""

from contextlib import contextmanager
from typing import Any

import numpy as np
import numpy.typing as npt

__all__ = ["padding1d", "to_distribution", "printoptions"]


def padding1d(
    n: int,
    v: npt.NDArray | None,
    padding_value: Any = 0,
    dtype: npt.DTypeLike | None = None,
) -> npt.NDArray:
    """Padding x to array of shape (n,).

    Parameters
    ----------
    n : int
        Size of vector.
    v : np.ndarray, optional
        Input vector.
    padding_value : any, default to `0`.
        If x.shape[0] is less than n, the rest will be filled with
        padding value.
    dtype : np.DTypeLike, optional
        Data type of array. If specify, cast x to dtype, else dtype of
        x will used, otherwise defaults to `~numpy.float32`.
    """

    dtype = dtype or (v is not None and v.dtype) or np.float32
    v = np.zeros(n, dtype=dtype) if v is None else v
    v = v.astype(dtype) if v.dtype != dtype else v
    assert v.ndim == 1

    if v.shape[0] >= n:
        return v[:n]

    padding = np.full(n - v.shape[0], padding_value, dtype=dtype)
    return np.concatenate([v, padding])


def to_distribution(values: npt.NDArray, step: float) -> npt.NDArray[np.int32]:
    indices = np.floor(values / step).astype(np.int32)
    dirtribution = np.zeros((indices.max() + 1), dtype=np.int32)
    for i in indices:
        dirtribution[i] = dirtribution[i] + 1

    return dirtribution


@contextmanager
def printoptions(*args, **kwargs):
    original_options = np.get_printoptions()
    np.set_printoptions(*args, **kwargs)

    try:
        yield
    finally:
        np.set_printoptions(**original_options)
