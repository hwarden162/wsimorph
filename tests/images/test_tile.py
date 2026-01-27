import numpy as np
import pytest

from wsimorph.images._tile import Tile
from wsimorph.images._wsi import WSI


def test_tile_validation():
    img = np.zeros((10, 10, 3))
    test_path = "tests/_test_data/small_tiff.tiff"
    wsi = WSI(test_path)

    with pytest.raises(TypeError, match="Image must be a numpy array."):
        Tile(123, 0, 0, 0, wsi)
    with pytest.raises(ValueError, match="Image must be a 3D numpy array."):
        Tile(np.zeros((10, 10)), 0, 0, 0, wsi)
    with pytest.raises(TypeError, match="Y start must be an integer."):
        Tile(img, "123", 0, 0, wsi)
    with pytest.raises(
        ValueError, match="Y start must be greater than or equal to zero."
    ):
        Tile(img, -1, 0, 0, wsi)
    with pytest.raises(TypeError, match="X start must be an integer."):
        Tile(img, 0, "123", 0, wsi)
    with pytest.raises(
        ValueError, match="X start must be greater than or equal to zero."
    ):
        Tile(img, 0, -1, 0, wsi)
    with pytest.raises(TypeError, match="Level must be an integer."):
        Tile(img, 0, 0, "123", wsi)
    with pytest.raises(
        ValueError,
        match="Level must be greater than or equal to zero and less than the level count of the parent WSI.",
    ):
        Tile(img, 0, 0, 123, wsi)
    with pytest.raises(TypeError, match="Parent WSI must be a WSI object."):
        Tile(img, 0, 0, 0, 123)
