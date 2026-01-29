from unittest.mock import MagicMock

import pytest
from openslide import OpenSlide
from wsimorph.image._wsi import _get_dimensions


def test_get_dimensions_valid_slide():
    """Test _get_dimensions with a valid OpenSlide object."""
    slide = MagicMock(spec=OpenSlide)
    slide.dimensions = (1000, 2000)

    result = _get_dimensions(slide)
    assert result == (1000, 2000)


def test_get_dimensions_invalid_slide_type():
    """Test _get_dimensions raises TypeError when the slide is not an OpenSlide."""
    with pytest.raises(TypeError, match="slide must be an OpenSlide object."):
        _get_dimensions("not_a_slide")


def test_get_dimensions_invalid_dimensions_type():
    """Test _get_dimensions raises TypeError for non-tuple dimensions."""
    slide = MagicMock(spec=OpenSlide)
    slide.dimensions = [1000, 2000]  # List instead of tuple

    with pytest.raises(TypeError, match="Dimensions are not a tuple of length 2."):
        _get_dimensions(slide)


def test_get_dimensions_invalid_dimensions_length():
    """Test _get_dimensions raises TypeError if dimensions tuple isn't length 2."""
    slide = MagicMock(spec=OpenSlide)
    slide.dimensions = (1000,)  # Tuple with one element

    with pytest.raises(TypeError, match="Dimensions are not a tuple of length 2."):
        _get_dimensions(slide)


def test_get_dimensions_non_integer_dimensions():
    """Test _get_dimensions raises TypeError when dimensions aren't integers."""
    slide = MagicMock(spec=OpenSlide)
    slide.dimensions = ("width", "height")  # Strings instead of integers

    with pytest.raises(TypeError, match="Dimensions are not integers."):
        _get_dimensions(slide)
