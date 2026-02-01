from pathlib import Path
import pytest

from wsimorph.image import WSI
from wsimorph.io import read_wsi

def test_read_wsi_validation():
    test_path_string = "tests/_test_data/small_tiff.tiff"
    test_path_path = Path(test_path_string)
    with pytest.raises(TypeError, match="Path must be a string or pathlib.Path object."):
        read_wsi(123)
