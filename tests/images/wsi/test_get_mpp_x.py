from unittest.mock import Mock

import pytest
from openslide import OpenSlide
from wsimorph.image._wsi import _get_mpp_x


def test_get_mpp_x_valid():
    slide = Mock(spec=OpenSlide)
    slide.properties = {"openslide.mpp-x": "0.254"}
    assert _get_mpp_x(slide) == 0.254


def test_get_mpp_x_default_value():
    slide = Mock(spec=OpenSlide)
    slide.properties = {}
    assert _get_mpp_x(slide) == 0.0


def test_get_mpp_x_invalid_slide_type():
    slide = Mock()
    with pytest.raises(TypeError, match="slide must be an OpenSlide object."):
        _get_mpp_x(slide)


def test_get_mpp_x_invalid_mpp_type():
    slide = Mock(spec=OpenSlide)
    slide.properties = {"openslide.mpp-x": "invalid"}
    with pytest.raises(ValueError):
        _get_mpp_x(slide)
