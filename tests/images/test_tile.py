import numpy as np
from pathlib import Path
import pytest

from wsimorph.image._tile import Tile
from wsimorph.image._wsi import WSI


def test_tile_validation():
    img = np.zeros((10, 10, 3))
    test_path = Path("tests/_test_data/small_tiff.tiff")
    wsi = WSI(test_path)
    with pytest.raises(TypeError, match="Parent WSI must be a WSI object."):
        Tile(img, 0, 0, 0, 0, 0, 0, 0, 123)
    with pytest.raises(TypeError, match="Level must be an integer."):
        Tile(img, 0, 0, "123", 0, 0, 0, 0, wsi)
    with pytest.raises(ValueError, match="Level must be greater than or equal to zero and less than the level count of the WSI."):
        Tile(img, 0, 0, -1, 0, 0, 0, 0, wsi)
    with pytest.raises(ValueError, match="Level must be greater than or equal to zero and less than the level count of the WSI."):
        Tile(img, 0, 0, 99999, 0, 0, 0, 0, wsi)
    with pytest.raises(TypeError, match="Image must be a numpy array."):
        Tile("not an array", 0, 0, 0, 0, 0, 0, 0, wsi)
    with pytest.raises(ValueError, match="Image must be a 3D numpy array."):
        Tile(np.zeros((10, 10)), 0, 0, 0, 0, 0, 0, 0, wsi)
    with pytest.raises(TypeError, match="Image must be a floating-point numpy array."):
        Tile(np.zeros((10, 10, 3), dtype=np.uint8), 0, 0, 0, 0, 0, 0, 0, wsi)
    with pytest.raises(ValueError, match="Image values must be between 0 and 1."):
        Tile(np.zeros((10, 10, 3)) - 1, 0, 0, 0, 0, 0, 0, 0, wsi)
    with pytest.raises(ValueError, match="Image values must be between 0 and 1."):
        Tile(np.zeros((10, 10, 3)) + 2, 0, 0, 0, 0, 0, 0, 0, wsi)
    with pytest.raises(TypeError, match="Start coordinates must be integers."):
        Tile(img, 0.5, 0, 0, 0, 0, 0, 0, wsi)
    with pytest.raises(TypeError, match="Start coordinates must be integers."):
        Tile(img, 0, 0.5, 0, 0, 0, 0, 0, wsi)
    with pytest.raises(ValueError, match="Start coordinates must be non-negative."):
        Tile(img, -1, 0, 0, 0, 0, 0, 0, wsi)
    with pytest.raises(ValueError, match="Start coordinates must be non-negative."):
        Tile(img, 0, -1, 0, 0, 0, 0, 0, wsi)
    with pytest.raises(ValueError, match="Image dimensions exceed the dimensions of the parent WSI."):
        Tile(img, 9999999, 0, 0, 0, 0, 0, 0, wsi)
    with pytest.raises(ValueError, match="Image dimensions exceed the dimensions of the parent WSI."):
        Tile(img, 0, 9999999, 0, 0, 0, 0, 0, wsi)
    with pytest.raises(TypeError, match="Padding values must be integers."):
        Tile(img, 0, 0, 0, 0.5, 0, 0, 0, wsi)
    with pytest.raises(TypeError, match="Padding values must be integers."):
        Tile(img, 0, 0, 0, 0, 0.5, 0, 0, wsi)
    with pytest.raises(TypeError, match="Padding values must be integers."):
        Tile(img, 0, 0, 0, 0, 0, 0.5, 0, wsi)
    with pytest.raises(TypeError, match="Padding values must be integers."):
        Tile(img, 0, 0, 0, 0, 0, 0, 0.5, wsi)
    with pytest.raises(ValueError, match="Padding values must be non-negative."):
        Tile(img, 0, 0, 0, -1, 0, 0, 0, wsi)
    with pytest.raises(ValueError, match="Padding values must be non-negative."):
        Tile(img, 0, 0, 0, 0, -1, 0, 0, wsi)
    with pytest.raises(ValueError, match="Padding values must be non-negative."):
        Tile(img, 0, 0, 0, 0, 0, -1, 0, wsi)
    with pytest.raises(ValueError, match="Padding values must be non-negative."):
        Tile(img, 0, 0, 0, 0, 0, 0, -1, wsi)
    with pytest.raises(ValueError, match="Padding values exceed the image dimensions."):
        Tile(img, 0, 0, 0, 10000000, 0, 0, 0, wsi)
    with pytest.raises(ValueError, match="Padding values exceed the image dimensions."):
        Tile(img, 0, 0, 0, 0, 0, 10000000, 0, wsi)
