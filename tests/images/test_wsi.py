import pytest

from wsimorph.images._wsi import WSI

def test_wsi_validation():
    test_path = "tests/_test_data/small_tiff.tiff"
    wsi = WSI(test_path)
    with pytest.raises(TypeError, match="Path must be a string."):
        WSI(123)
    with pytest.raises(FileNotFoundError, match="File not found."):
        WSI("tests/_test_data/nonexistent.tiff")
    with pytest.raises(TypeError, match="Microns must be a float."):
        wsi.pixels_from_microns("123", 0)
    with pytest.raises(ValueError, match="Level must be greater than or equal to zero and less than the level count of the WSI."):
        wsi.pixels_from_microns(123, 123)
    with pytest.raises(ValueError, match="Microns must be greater than zero."):
        wsi.pixels_from_microns(0, 0)
    with pytest.raises(ValueError, match="WSI has no pixel size information."):
        wsi._mpp = 0
        wsi.pixels_from_microns(123, 0)

def test_wsi_pixels_from_microns():
    test_path = "tests/_test_data/small_tiff.tiff"
    wsi = WSI(test_path)
    assert wsi.pixels_from_microns(123, 0) == 123 / 0.499

