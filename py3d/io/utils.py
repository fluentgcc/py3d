# pyre-unsafe

import contextlib
import pathlib
import warnings
from typing import cast, ContextManager, IO, Optional, Union

import numpy as np
from PIL import Image


PathOrStr = Union[pathlib.Path, str]


def _open_file(f, mode: str = "r") -> ContextManager[IO]:
    if isinstance(f, pathlib.Path):
        f = f.open(mode)
        return contextlib.closing(f)
    else:
        return contextlib.nullcontext(cast(IO, f))
    
def _make_array(data, cols: int, dtype: np.dtype) -> np.ndarray:
    """
    Return a 2D array with the specified cols and dtype filled with data,
    even when data is empty.
    """
    if not len(data):
        return np.zeros((0, cols), dtype=dtype)

    return np.array(data, dtype=dtype)

def _check_faces_indices(
    faces_indices: np.ndarray, max_index: int, pad_value: Optional[int] = None
) -> np.ndarray:
    if pad_value is None:
        mask = np.ones(faces_indices.shape[:-1]).bool()  # Keep all faces
    else:
        mask = faces_indices.ne(pad_value).any(dim=-1)
    if np.any(faces_indices[mask] >= max_index) or np.any(
        faces_indices[mask] < 0
    ):
        warnings.warn("Faces have invalid indices")
    return faces_indices


def _read_image(file_name: str, format=None):
    """
    Read an image from a file using Pillow.
    Args:
        file_name: image file path.
        path_manager: PathManager for interpreting file_name.
        format: one of ["RGB", "BGR"]
    Returns:
        image: an image of shape (H, W, C).
    """
    if format not in ["RGB", "BGR"]:
        raise ValueError("format can only be one of [RGB, BGR]; got %s", format)
    with open(file_name, "rb") as f:
        image = Image.open(f)
        if format is not None:
            # PIL only supports RGB. First convert to RGB and flip channels
            # below for BGR.
            image = image.convert("RGB")
        image = np.asarray(image).astype(np.float32)
        if format == "BGR":
            image = image[:, :, ::-1]
        return image