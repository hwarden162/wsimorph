import pytest
from wsimorph.image._wsi import _get_mpp


def test_get_mpp_valid_equal_values():
    result = _get_mpp(0.25, 0.25)
    assert result == 0.25


def test_get_mpp_valid_unequal_values():
    result = _get_mpp(0.25, 0.30)
    assert result == 0.0


def test_get_mpp_zero_values():
    result = _get_mpp(0.0, 0.25)
    assert result == 0.0

    result = _get_mpp(0.25, 0.0)
    assert result == 0.0

    result = _get_mpp(0.0, 0.0)
    assert result == 0.0


def test_get_mpp_invalid_types():
    with pytest.raises(TypeError):
        _get_mpp("0.25", 0.25)

    with pytest.raises(TypeError):
        _get_mpp(0.25, "0.25")

    with pytest.raises(TypeError):
        _get_mpp("0.25", "0.25")


def test_get_mpp_identical_nonzero_values():
    result = _get_mpp(10.0, 10.0)
    assert result == 10.0
