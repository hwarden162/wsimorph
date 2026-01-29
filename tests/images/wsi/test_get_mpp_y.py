from unittest.mock import MagicMock

import pytest
from openslide import OpenSlide
from wsimorph.image._wsi import _get_mpp_y


def test_get_mpp_y_valid_property():
    slide = MagicMock(spec=OpenSlide)
    slide.properties = {"openslide.mpp-y": "0.25"}

    result = _get_mpp_y(slide)
    assert result == 0.25


def test_get_mpp_y_missing_property():
    slide = MagicMock(spec=OpenSlide)
    slide.properties = {}

    result = _get_mpp_y(slide)
    assert result == 0.0


def test_get_mpp_y_invalid_slide_type():
    non_slide = "Not an OpenSlide object"

    with pytest.raises(TypeError, match="slide must be an OpenSlide object."):
        _get_mpp_y(non_slide)


def test_get_mpp_y_invalid_mpp_type():
    slide = MagicMock(spec=OpenSlide)
    slide.properties = {"openslide.mpp-y": "not a float"}

    with pytest.raises(ValueError, match="could not convert string to float"):
        _get_mpp_y(slide)
