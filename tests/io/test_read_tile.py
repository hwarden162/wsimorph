from pathlib import Path
import pytest
from re import escape

from wsimorph.image import WSI
from wsimorph.io import read_tile

def test_read_tile_validation():
    test_path = Path("tests/_test_data/small_tiff.tiff")
    wsi = WSI(test_path)
    with pytest.raises(TypeError, match="wsi must be a WSI object."):
        read_tile(123, 0, 0, 0, 100, 100, 0)
    with pytest.raises(TypeError, match="level must be an integer."):
        read_tile(wsi, 0.5, 0, 100, 100, 100, padding=0)
    with pytest.raises(ValueError, match="level must be greater than or equal to zero and less than the level count of the WSI."):
        read_tile(wsi, -1, 0, 100, 100, 100, padding=0)
    with pytest.raises(ValueError, match="level must be greater than or equal to zero and less than the level count of the WSI."):
        read_tile(wsi, 9999999, 0, 100, 100, 100, padding=0)
    with pytest.raises(TypeError, match="y_start and x_start must be integers."):
        read_tile(wsi, 0, 0.5, 0, 100, 100, padding=0)
    with pytest.raises(TypeError, match="y_start and x_start must be integers."):
        read_tile(wsi, 0, 0, 0.5, 100, 100, padding=0)
    with pytest.raises(ValueError, match="y_start and x_start must be non-negative."):
        read_tile(wsi, 0, -1, 0, 100, 100, padding=0)
    with pytest.raises(ValueError, match="y_start and x_start must be non-negative."):
        read_tile(wsi, 0, 0, -1, 100, 100, padding=0)
    with pytest.raises(TypeError, match="y_len and x_len must be integers."):
        read_tile(wsi, 0, 0, 0, 0.5, 100, padding=0)
    with pytest.raises(TypeError, match="y_len and x_len must be integers."):
        read_tile(wsi, 0, 0, 0, 100, 0.5, padding=0)
    with pytest.raises(ValueError, match="y_len and x_len must be positive."):
        read_tile(wsi, 0, 0, 0, 0, 100, padding=0)
    with pytest.raises(ValueError, match="y_len and x_len must be positive."):
        read_tile(wsi, 0, 0, 0, 100, 0, padding=0)
    with pytest.raises(ValueError, match=escape("y_start + y_len exceeds the level dimensions or x_start + x_len exceeds the level dimensions.")):
        read_tile(wsi, 0, 9999999, 0, 100, 100, padding=0)
    with pytest.raises(ValueError, match=escape("y_start + y_len exceeds the level dimensions or x_start + x_len exceeds the level dimensions.")):
        read_tile(wsi, 0, 0, 9999999, 100, 100, padding=0)
    with pytest.raises(TypeError, match="padding must be an integer."):
        read_tile(wsi, 0, 0, 0, 100, 100, 0.5)
    with pytest.raises(ValueError, match="padding must be non-negative."):
        read_tile(wsi, 0, 0, 0, 100, 100, -1)
