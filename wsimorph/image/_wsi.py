from pathlib import Path

from openslide import OpenSlide


def _get_vendor(slide: OpenSlide) -> str:
    """
    Determines the vendor of the provided OpenSlide object by retrieving the
    "openslide.vendor" property. If the property is not found, "Unknown" is returned.
    Ensures that the returned value is a string.

    :param slide: OpenSlide object whose vendor is to be determined.
    :type slide: OpenSlide
    :return: The vendor name of the slide or "Unknown" if not available.
    :rtype: str
    :raises TypeError: If the provided object is not an instance of OpenSlide or
        if the retrieved vendor value is not a string.
    """
    if not isinstance(slide, OpenSlide):
        raise TypeError("slide must be an OpenSlide object.")
    vendor = slide.properties.get("openslide.vendor", "Unknown")
    if not isinstance(vendor, str):
        raise TypeError("Vendor name is not a string.")
    return vendor


def _get_level_count(slide: OpenSlide) -> int:
    """
    Calculates and retrieves the number of levels available in an OpenSlide object.
    The function validates the input type and ensures that the retrieved level count
    is an integer.

    :param slide: The OpenSlide object from which the level count will be retrieved.
    :type slide: OpenSlide
    :return: The level count of the OpenSlide object.
    :rtype: int
    :raises TypeError: If `slide` is not an OpenSlide object or the level count is not
                       an integer.
    """
    if not isinstance(slide, OpenSlide):
        raise TypeError("slide must be an OpenSlide object.")
    level_count = slide.level_count
    if not isinstance(level_count, int):
        raise TypeError("Level count is not an integer.")
    return level_count


def _get_dimensions(slide: OpenSlide) -> tuple[int, int]:
    """
    Retrieves the dimensions of a given OpenSlide slide object. The function ensures
    that the provided slide is an instance of `OpenSlide` and validates the dimensions
    attribute to confirm it is a tuple containing two integers.

    :param slide: An OpenSlide instance from which to retrieve dimensions.
    :type slide: OpenSlide
    :return: A tuple representing the dimensions of the slide, where the first element
        is the width and the second is the height.
    :rtype: tuple[int, int]
    :raises TypeError: If the slide is not an instance of `OpenSlide`, or if the
        dimensions are not formatted correctly as a tuple of two integers.
    """
    if not isinstance(slide, OpenSlide):
        raise TypeError("slide must be an OpenSlide object.")
    dimensions = slide.dimensions
    if not isinstance(dimensions, tuple) or len(dimensions) != 2:
        raise TypeError("Dimensions are not a tuple of length 2.")
    if not isinstance(dimensions[0], int) or not isinstance(dimensions[1], int):
        raise TypeError("Dimensions are not integers.")
    return dimensions


def _get_level_dimensions(slide: OpenSlide) -> tuple[tuple[int, int], ...]:
    """
    Extracts and validates the level dimensions of an OpenSlide object.

    This function retrieves the level dimensions from the provided OpenSlide object,
    ensures that the dimensions are in the correct format, and validates that they
    consist of tuples of length 2, where each element is an integer.

    :param slide: The OpenSlide object from which level dimensions are extracted.
    :type slide: OpenSlide
    :return: A tuple containing tuples of level dimensions, with each inner tuple
        representing the width and height of a specific level.
    :rtype: tuple[tuple[int, int], ...]
    :raises TypeError: If the slide is not an OpenSlide object, if the level dimensions
        are not a tuple, if the dimensions do not consist of tuples of length 2,
        or if any of the inner dimension values are not integers.
    """
    if not isinstance(slide, OpenSlide):
        raise TypeError("slide must be an OpenSlide object.")
    level_dimensions = slide.level_dimensions
    if not isinstance(level_dimensions, tuple):
        raise TypeError("Level dimensions are not a tuple.")
    for level_dim in level_dimensions:
        if not isinstance(level_dim, tuple) or len(level_dim) != 2:
            raise TypeError("Level dimensions are not tuples of length 2.")
        if not isinstance(level_dim[0], int) or not isinstance(level_dim[1], int):
            raise TypeError("Level dimensions are not integers.")
    return level_dimensions


def _get_level_downsamples(slide: OpenSlide) -> tuple[float, ...]:
    """
    Retrieves the level downsamples from an OpenSlide object.

    This function ensures the provided object is of type OpenSlide and that its
    level_downsamples attribute is a tuple of floats. It raises a TypeError for
    invalid types.

    :param slide: The OpenSlide object from which to retrieve level downsamples.
    :type slide: OpenSlide
    :return: A tuple of floats representing the level downsamples from the
        OpenSlide object.
    :rtype: tuple[float, ...]
    :raises TypeError: If the provided slide is not an OpenSlide object, if
        the level_downsamples attribute is not a tuple, or if the elements
        in the level_downsamples are not floats.
    """
    if not isinstance(slide, OpenSlide):
        raise TypeError("slide must be an OpenSlide object.")
    level_downsamples = slide.level_downsamples
    if not isinstance(level_downsamples, tuple):
        raise TypeError("Level downsamples are not a tuple.")
    for level_downsample in level_downsamples:
        if not isinstance(level_downsample, float):
            raise TypeError("Level downsamples are not floats.")
    return level_downsamples


def _get_mpp_y(slide: OpenSlide) -> float:
    """
    Calculate the microns per pixel (MPP) in the y-direction (vertical) of a given
    OpenSlide object. The function retrieves the property `openslide.mpp-y` from
    the slide's properties and returns its value as a float. If the `mpp-y`
    property is not available, the function defaults to a value of 0.0.

    :param slide: The OpenSlide object from which the `mpp-y` property is retrieved.
                  It must be an instance of the `OpenSlide` class.
    :type slide: OpenSlide

    :return: The microns per pixel (MPP) in the y-direction as a float. If the
             property is unavailable, 0.0 is returned by default.
    :rtype: float

    :raises TypeError: If the provided `slide` is not an OpenSlide object or if the
                       retrieved `mpp-y` property is not a `float`.
    """
    if not isinstance(slide, OpenSlide):
        raise TypeError("slide must be an OpenSlide object.")
    mpp_y = float(slide.properties.get("openslide.mpp-y", 0.0))
    if not isinstance(mpp_y, float):
        raise TypeError("mpp-y is not a float.")
    return mpp_y


def _get_mpp_x(slide: OpenSlide) -> float:
    """
    Get the microns per pixel (mpp) value along the X-axis from an OpenSlide object.

    This function retrieves the "openslide.mpp-x" property from the provided
    OpenSlide object. If the property does not exist, a default value of 0.0 is
    returned. The function also ensures that the returned mpp-x value is of type
    float.

    :param slide: The OpenSlide object from which the "openslide.mpp-x" property
                  will be retrieved.
    :type slide: OpenSlide
    :return: The "openslide.mpp-x" value of the slide, defaulting to 0.0 if not
             present.
    :rtype: float
    :raises TypeError: If the input slide is not an OpenSlide object or if the
                       retrieved "openslide.mpp-x" value is not a float.
    """
    if not isinstance(slide, OpenSlide):
        raise TypeError("slide must be an OpenSlide object.")
    mpp_x = float(slide.properties.get("openslide.mpp-x", 0.0))
    if not isinstance(mpp_x, float):
        raise TypeError("mpp-x is not a float.")
    return mpp_x


def _get_mpp(mpp_y: float, mpp_x: float) -> float:
    """
    Calculate and validate the microns-per-pixel (MPP) value.

    This function checks whether the MPP values are valid floats and ensures
    that the two input values are equal. If either MPP value is zero or they
    are not equal, it returns 0.0.

    :param mpp_y: Microns-per-pixel value along the y-axis.
    :type mpp_y: float
    :param mpp_x: Microns-per-pixel value along the x-axis.
    :type mpp_x: float
    :return: The microns-per-pixel value if both inputs are valid and equal;
             otherwise, returns 0.0.
    :rtype: float
    :raises TypeError: If the provided `mpp_y` or `mpp_x` are not of type
                       float.
    """
    if not isinstance(mpp_y, float) or not isinstance(mpp_x, float):
        raise TypeError("mpp-y and mpp-x must be floats.")
    if mpp_y == 0 or mpp_x == 0:
        return 0.0
    if mpp_y != mpp_x:
        return 0.0
    return mpp_y


class WSI:
    """
    Represents a Whole Slide Image (WSI) file.

    This class provides an interface for accessing and handling properties of a
    whole slide image file. It validates the file path during initialization and
    extracts metadata such as dimensions, resolution, and downsampling factors.
    Instances of this class allow access to various attributes like image
    dimensions, microns per pixel, and vendor information.

    :ivar path: The file path of the WSI.
    :type path: Path
    :ivar name: The file name of the WSI.
    :type name: str
    :ivar stem: The name of the WSI file without its extension.
    :type stem: str
    :ivar vendor: The vendor of the WSI.
    :type vendor: str
    :ivar level_count: The number of resolution levels in the WSI.
    :type level_count: int
    :ivar dimensions: The dimensions (width, height) of the WSI at the highest resolution level.
    :type dimensions: tuple[int, int]
    :ivar level_dimensions: The dimensions (width, height) of the WSI at each resolution level.
    :type level_dimensions: tuple[tuple[int, int], ...]
    :ivar level_downsamples: The downsampling factors for each resolution level.
    :type level_downsamples: tuple[float, ...]
    :ivar mpp_y: The microns per pixel value in the vertical direction.
    :type mpp_y: float
    :ivar mpp_x: The microns per pixel value in the horizontal direction.
    :type mpp_x: float
    :ivar mpp: The overall microns per pixel value for the WSI.
    :type mpp: float
    """

    def __init__(self, path: Path) -> None:
        """
        Initializes an instance of the class representing a Whole Slide Image (WSI) file.

        This constructor verifies the validity of the given file path and extracts
        necessary metadata about the WSI using the OpenSlide library.

        :param path: The file system path to the WSI file.
        :type path: Path
        :raises TypeError: If the provided path is not a pathlib.Path object.
        :raises FileNotFoundError: If the provided path does not exist.
        """
        if not isinstance(path, Path):
            raise TypeError("Path must be a pathlib.Path object.")
        if not path.exists():
            raise FileNotFoundError("Given WSI file path does not exist.")
        self._path: Path = path
        self._name: str = path.name
        self._stem: str = path.stem
        with OpenSlide(path) as slide:
            self._vendor: str = _get_vendor(slide)
            self._level_count: int = _get_level_count(slide)
            self._dimensions: tuple[int, int] = _get_dimensions(slide)
            self._level_dimensions: tuple[tuple[int, int], ...] = _get_level_dimensions(
                slide
            )
            self._level_downsamples: tuple[float, ...] = _get_level_downsamples(slide)
            self._mpp_y: float = _get_mpp_y(slide)
            self._mpp_x: float = _get_mpp_x(slide)
            self._mpp: float = _get_mpp(self._mpp_y, self._mpp_x)

    def pixels_from_microns(self, microns: float, level: int = 0) -> float:
        """
        Converts a microns measurement to pixels based on the specified level of the WSI
        (Whole Slide Image). This method computes the equivalent pixels for the given microns
        value considering the level's downsample factor and the microns-per-pixel (MPP) ratio
        of the WSI. It validates inputs and ensures they fit within acceptable ranges and types.

        :param microns: The measurement in microns to be converted.
        :type microns: float
        :param level: The level of the WSI to perform the conversion. Defaults to 0.
        :type level: int
        :return: The equivalent pixel measurement.
        :rtype: float
        :raises TypeError: If `microns` is not a float or if `level` is not an integer.
        :raises ValueError: If `microns` is less than or equal to zero,
                            if `level` is out of valid range,
                            or if the WSI lacks pixel size information.
        """
        if isinstance(microns, int):
            microns = float(microns)
        if not isinstance(microns, float):
            raise TypeError("Microns must be a float.")
        if microns <= 0:
            raise ValueError("Microns must be greater than zero.")
        if not isinstance(level, int):
            raise TypeError("Level must be an integer.")
        if level < 0 or level >= self._level_count:
            raise ValueError(
                f"Level must be greater than or equal to zero and less than the level count of the WSI ({self._level_count})."
            )
        if self._mpp == 0:
            raise ValueError("WSI has no pixel size information.")
        return microns / (self._mpp * self._level_downsamples[level])

    @property
    def path(self) -> Path:
        return self._path

    @property
    def name(self) -> str:
        return self._name

    @property
    def stem(self) -> str:
        return self._stem

    @property
    def vendor(self) -> str:
        return self._vendor

    @property
    def level_count(self) -> int:
        return self._level_count

    @property
    def dimensions(self) -> tuple[int, int]:
        return self._dimensions

    @property
    def level_dimensions(self) -> tuple[tuple[int, int], ...]:
        return self._level_dimensions

    @property
    def level_downsamples(self) -> tuple[float, ...]:
        return self._level_downsamples

    @property
    def mpp_y(self) -> float:
        return self._mpp_y

    @property
    def mpp_x(self) -> float:
        return self._mpp_x

    @property
    def mpp(self) -> float:
        return self._mpp

    def __repr__(self) -> str:
        return f"<WSI: {self.name}>"
