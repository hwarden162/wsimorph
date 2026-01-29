from unittest.mock import MagicMock

import pytest
from openslide import OpenSlide
from wsimorph.image._wsi import _get_level_downsamples


def test_get_level_downsamples_valid_input():
    slide_mock = MagicMock(spec=OpenSlide)
    slide_mock.level_downsamples = (0.5, 1.0, 2.0)
    result = _get_level_downsamples(slide_mock)
    assert result == (0.5, 1.0, 2.0)


def test_get_level_downsamples_invalid_slide_type():
    with pytest.raises(TypeError, match="slide must be an OpenSlide object."):
        _get_level_downsamples("not an OpenSlide object")


def test_get_level_downsamples_level_downsamples_not_tuple():
    slide_mock = MagicMock(spec=OpenSlide)
    slide_mock.level_downsamples = [0.5, 1.0, 2.0]  # Not a tuple
    with pytest.raises(TypeError, match="Level downsamples are not a tuple."):
        _get_level_downsamples(slide_mock)


def test_get_level_downsamples_level_downsamples_not_all_floats():
    slide_mock = MagicMock(spec=OpenSlide)
    slide_mock.level_downsamples = (0.5, "1.0", 2.0)  # Contains a string
    with pytest.raises(TypeError, match="Level downsamples are not floats."):
        _get_level_downsamples(slide_mock)
