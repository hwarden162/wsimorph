import numpy as np

from ._wsi import WSI


class Tile:
    """
    Represents a single image tile extracted from a whole-slide image (WSI).

    Provides access to the image tile and associated metadata, such as its
    position, resolution level, and parent WSI. This class ensures the image
    data is validated and normalized for compatibility with downstream processing.

    :ivar image: The 3D image ndarray representing the tile data. Must be normalized
        to the range [0, 1].
    :type image: numpy.ndarray
    :ivar y_start: The y-coordinate of the top-left corner of the tile in the
        parent WSI. Must be a non-negative integer.
    :type y_start: int
    :ivar x_start: The x-coordinate of the top-left corner of the tile in the
        parent WSI. Must be a non-negative integer.
    :type x_start: int
    :ivar level: The resolution level of the tile in the parent WSI. Must be an
        integer between 0 (highest resolution) and the maximum level supported by
        the parent WSI, exclusive.
    :type level: int
    :ivar parent_wsi: Reference to the parent WSI object from which the tile
        was extracted.
    :type parent_wsi: WSI
    :ivar num_channels: Number of color channels in the image tile. Typically
        corresponds to the last axis of the image data.
    :type num_channels: int
    """
    def __init__(
        self, image: np.ndarray, y_start: int, x_start: int, level: int, parent_wsi: WSI
    ):
        """
        Initializes the object with the given image patch and related metadata.

        :param image: A 3D ndarray containing the image patch data. Must be in a compatible
            format and normalized to the range [0, 1].
        :param y_start: The y-coordinate of the top-left corner of the image patch within
            the parent whole-slide image. Must be a non-negative integer.
        :param x_start: The x-coordinate of the top-left corner of the image patch within
            the parent whole-slide image. Must be a non-negative integer.
        :param level: The resolution level at which the image patch resides within the
            parent whole-slide image. Must be an integer greater than or equal to zero
            and less than the level count of the parent whole-slide image.
        :param parent_wsi: The parent whole-slide image (WSI) object that provides context
            for the image patch. Must be a valid instance of the WSI class.

        :raises TypeError: Raised if `image` is not a numpy ndarray, `y_start` or `x_start`
            is not an integer, or `parent_wsi` is not an instance of the WSI class.
        :raises ValueError: Raised if `image` is not a 3D array, `y_start` or `x_start` is
            not non-negative, `level` is not within valid bounds, `image` does not have a
            compatible dtype, or if it is not normalized to the range [0, 1].
        """
        if not isinstance(image, np.ndarray):
            raise TypeError("Image must be a numpy array.")
        if not image.ndim == 3:
            raise ValueError("Image must be a 3D numpy array.")
        if not isinstance(y_start, int):
            raise TypeError("Y start must be an integer.")
        if not y_start >= 0:
            raise ValueError("Y start must be greater than or equal to zero.")
        if not isinstance(x_start, int):
            raise TypeError("X start must be an integer.")
        if not x_start >= 0:
            raise ValueError("X start must be greater than or equal to zero.")
        if not isinstance(level, int):
            raise TypeError("Level must be an integer.")
        if not isinstance(parent_wsi, WSI):
            raise TypeError("Parent WSI must be a WSI object.")
        if level < 0 or level >= parent_wsi.level_count:
            raise ValueError(
                "Level must be greater than or equal to zero and less than the level count of the parent WSI."
            )
        if image.dtype == np.uint8:
            image = image.astype(np.float32) / 255
        if image.dtype == np.uint16:
            image = image.astype(np.float32) / 65535
        if not np.issubdtype(image.dtype, np.floating): raise TypeError("Image must be a of a compatible dtype.")
        if (image.max() > 1) or (image.min() < 0): raise ValueError("Image must be normalized to [0, 1].")
        self._image = image
        self._y_start = y_start
        self._x_start = x_start
        self._level = level
        self._parent_wsi = parent_wsi
        self._num_channels = image.shape[2]

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
    def parent_wsi(self) -> WSI:
        return self._parent_wsi

    @property
    def num_channels(self) -> int:
        return self._num_channels
