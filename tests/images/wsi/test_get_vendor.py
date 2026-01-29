from unittest.mock import Mock

import pytest
from openslide import OpenSlide
from wsimorph.image._wsi import _get_vendor


def test_get_vendor_success():
    slide = Mock(spec=OpenSlide)
    slide.properties = {"openslide.vendor": "VendorName"}
    result = _get_vendor(slide)
    assert result == "VendorName"


def test_get_vendor_unknown():
    slide = Mock(spec=OpenSlide)
    slide.properties = {}
    result = _get_vendor(slide)
    assert result == "Unknown"


def test_get_vendor_invalid_slide_object():
    with pytest.raises(TypeError, match="slide must be an OpenSlide object."):
        _get_vendor(None)


def test_get_vendor_invalid_vendor_type():
    slide = Mock(spec=OpenSlide)
    slide.properties = {"openslide.vendor": 123}
    with pytest.raises(TypeError, match="Vendor name is not a string."):
        _get_vendor(slide)
