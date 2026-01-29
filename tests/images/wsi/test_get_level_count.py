from unittest.mock import Mock

import pytest
from openslide import OpenSlide
from wsimorph.image._wsi import _get_level_count


def test_get_level_count_valid_slide():
    # Mock an OpenSlide object with valid level_count
    mock_slide = Mock(spec=OpenSlide)
    mock_slide.level_count = 3

    # Validate the output of _get_level_count
    result = _get_level_count(mock_slide)
    assert result == 3


def test_get_level_count_invalid_slide_type():
    # Test with an invalid slide type (not an OpenSlide object)
    with pytest.raises(TypeError, match="slide must be an OpenSlide object."):
        _get_level_count("not_a_slide")


def test_get_level_count_non_integer_level_count():
    # Mock an OpenSlide object with a non-integer level_count
    mock_slide = Mock(spec=OpenSlide)
    mock_slide.level_count = "three"

    # Validate that a TypeError is raised
    with pytest.raises(TypeError, match="Level count is not an integer."):
        _get_level_count(mock_slide)


def test_get_level_count_zero_levels():
    # Mock an OpenSlide object with zero levels
    mock_slide = Mock(spec=OpenSlide)
    mock_slide.level_count = 0

    # Validate the output of _get_level_count
    result = _get_level_count(mock_slide)
    assert result == 0
