# File: tests/test__wsi.py

from unittest.mock import Mock

import pytest
from openslide import OpenSlide
from wsimorph.image._wsi import _get_level_dimensions


def test_get_level_dimensions_valid_input():
    slide_mock = Mock(spec=OpenSlide)
    slide_mock.level_dimensions = ((1000, 500), (500, 250), (250, 125))

    result = _get_level_dimensions(slide_mock)

    assert result == ((1000, 500), (500, 250), (250, 125))


def test_get_level_dimensions_invalid_object_type():
    with pytest.raises(TypeError, match="slide must be an OpenSlide object."):
        _get_level_dimensions("not_an_openslide_object")


def test_get_level_dimensions_invalid_level_dimensions_type():
    slide_mock = Mock(spec=OpenSlide)
    slide_mock.level_dimensions = [1000, 500]

    with pytest.raises(TypeError, match="Level dimensions are not a tuple."):
        _get_level_dimensions(slide_mock)


def test_get_level_dimensions_invalid_inner_tuple_length():
    slide_mock = Mock(spec=OpenSlide)
    slide_mock.level_dimensions = ((1000, 500), (500,), (250, 125))

    with pytest.raises(TypeError, match="Level dimensions are not tuples of length 2."):
        _get_level_dimensions(slide_mock)


def test_get_level_dimensions_invalid_inner_tuple_value_type():
    slide_mock = Mock(spec=OpenSlide)
    slide_mock.level_dimensions = ((1000, "500"), (500, 250), (250, 125))

    with pytest.raises(TypeError, match="Level dimensions are not integers."):
        _get_level_dimensions(slide_mock)
