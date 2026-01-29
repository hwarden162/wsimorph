import numpy as np
import pytest

from wsimorph.image._tile import Tile
from wsimorph.image._wsi import WSI


def test_tile_validation():
    img = np.zeros((10, 10, 3))
    test_path = "tests/_test_data/small_tiff.tiff"
    wsi = WSI(test_path)
