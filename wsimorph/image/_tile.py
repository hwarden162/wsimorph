import numpy as np

from ._wsi import WSI


class Tile:
    """
    Represents a tile extracted from a whole-slide image (WSI).

    This class defines the attributes and properties of an extracted image tile
    from a WSI. It offers convenient access to the tile's image data, spatial
    coordinates, magnification level, and padding information. The `Tile` class is
    intended to work within a WSI processing context, ensuring compatibility with
    the parent image and managing constraints such as valid coordinates and padding.

    :ivar image: The 3D numpy array representing the tile image.
    :type image: np.ndarray
    :ivar y_start: The starting y-coordinate of the tile within the parent WSI.
    :type y_start: int
    :ivar x_start: The starting x-coordinate of the tile within the parent WSI.
    :type x_start: int
    :ivar level: The magnification level of the tile within the WSI.
    :type level: int
    :ivar ylo_pad: The vertical padding at the lower boundary of the tile.
    :type ylo_pad: int
    :ivar yhi_pad: The vertical padding at the upper boundary of the tile.
    :type yhi_pad: int
    :ivar xlo_pad: The horizontal padding at the left boundary of the tile.
    :type xlo_pad: int
    :ivar xhi_pad: The horizontal padding at the right boundary of the tile.
    :type xhi_pad: int
    """

    def __init__(
        self,
        image: np.ndarray,
        y_start: int,
        x_start: int,
        level: int,
        ylo_pad: int,
        yhi_pad: int,
        xlo_pad: int,
        xhi_pad: int,
        parent_wsi: WSI,
    ):
        """
        Initializes an object with an image, starting coordinates, level, padding
        values, and a parent whole-slide image (WSI). This constructor ensures all
        provided parameters meet required conditions for compatibility with the
        parent WSI and internal constraints.

        :param image: A 3D numpy array representing the image region.
        :param y_start: Starting y-coordinate for the image region within the
                        parent WSI.
        :param x_start: Starting x-coordinate for the image region within the
                        parent WSI.
        :param level: Magnification level of the WSI at which the image is located.
        :param ylo_pad: Amount of vertical padding at the lower boundary.
        :param yhi_pad: Amount of vertical padding at the upper boundary.
        :param xlo_pad: Amount of horizontal padding at the left boundary.
        :param xhi_pad: Amount of horizontal padding at the right boundary.
        :param parent_wsi: Parent whole-slide image (WSI) object associated with
                           the image.

        :raises TypeError: If any parameter is of an incorrect type.
        :raises ValueError: If any parameter value does not meet required constraints.
        """
        if not isinstance(parent_wsi, WSI):
            raise TypeError("Parent WSI must be a WSI object.")
        if not isinstance(level, int):
            raise TypeError("Level must be an integer.")
        if level < 0 or level >= parent_wsi.level_count:
            raise ValueError(
                "Level must be greater than or equal to zero and less than the level count of the WSI."
            )
        if not isinstance(image, np.ndarray):
            raise TypeError("Image must be a numpy array.")
        if image.ndim != 3:
            raise ValueError("Image must be a 3D numpy array.")
        if not np.issubdtype(image.dtype, np.floating):
            raise TypeError("Image must be a floating-point numpy array.")
        if image.min() < 0 or image.max() > 1:
            raise ValueError("Image values must be between 0 and 1.")
        if not isinstance(y_start, int) or not isinstance(x_start, int):
            raise TypeError("Start coordinates must be integers.")
        if y_start < 0 or x_start < 0:
            raise ValueError("Start coordinates must be non-negative.")
        if (
            image.shape[0] + y_start > parent_wsi.level_dimensions[level][0]
            or image.shape[1] + x_start > parent_wsi.level_dimensions[level][1]
        ):
            raise ValueError(
                "Image dimensions exceed the dimensions of the parent WSI."
            )
        if (
            not isinstance(ylo_pad, int)
            or not isinstance(yhi_pad, int)
            or not isinstance(xlo_pad, int)
            or not isinstance(xhi_pad, int)
        ):
            raise TypeError("Padding values must be integers.")
        if ylo_pad < 0 or yhi_pad < 0 or xlo_pad < 0 or xhi_pad < 0:
            raise ValueError("Padding values must be non-negative.")
        if ylo_pad + yhi_pad > image.shape[0] or xlo_pad + xhi_pad > image.shape[1]:
            raise ValueError("Padding values exceed the image dimensions.")
        self._image = image
        self._y_start = y_start
        self._x_start = x_start
        self._level = level
        self._ylo_pad = ylo_pad
        self._yhi_pad = yhi_pad
        self._xlo_pad = xlo_pad
        self._xhi_pad = xhi_pad

    @property
    def image(self) -> np.ndarray:
        return self._image

    @property
    def y_start(self) -> int:
        return self._y_start

    @property
    def x_start(self) -> int:
        return self._x_start

    @property
    def level(self) -> int:
        return self._level

    @property
    def ylo_pad(self) -> int:
        return self._ylo_pad

    @property
    def yhi_pad(self) -> int:
        return self._yhi_pad

    @property
    def xlo_pad(self) -> int:
        return self._xlo_pad

    @property
    def xhi_pad(self) -> int:
        return self._xhi_pad
