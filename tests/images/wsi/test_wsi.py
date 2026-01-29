from pathlib import Path

import pytest
from wsimorph.image._wsi import WSI


def test_wsi_initialization_invalid_path_type():
    with pytest.raises(TypeError, match="Path must be a pathlib.Path object."):
        WSI("invalid_path_string")


def test_wsi_initialization_nonexistent_path():
    nonexistent_path = Path("/nonexistent/path/to/file.tiff")
    with pytest.raises(FileNotFoundError, match="Given WSI file path does not exist."):
        WSI(nonexistent_path)

def test_wsi_initialization_values():
    test_path = Path("tests/_test_data/small_tiff.tiff")
    wsi = WSI(test_path)
    assert wsi._path == test_path
    assert wsi._name == "small_tiff.tiff"
    assert wsi._stem == "small_tiff"
    assert wsi._vendor == "aperio"
    assert wsi._level_count == 1
    assert wsi._dimensions == (2220, 2967)
    assert wsi._level_dimensions == ((2220, 2967),)
    assert wsi._level_downsamples == (1.0,)
    assert wsi._mpp_y == 0.499
    assert wsi._mpp_x == 0.499
    assert wsi._mpp == 0.499
