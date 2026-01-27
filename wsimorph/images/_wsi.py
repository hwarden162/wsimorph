from pathlib import Path

from openslide import OpenSlide


class WSI:
    """
    Represents a Whole Slide Image (WSI) object.

    This class provides functionalities to interact with whole slide images
    by extracting metadata like vendor, dimensions, level details, and pixel
    spacing (microns per pixel). It also facilitates converting microns to
    pixels based on slide magnification information.

    :ivar path: The file path to the WSI as a Path object.
    :type path: Path
    :ivar name: The file name of the WSI.
    :type name: str
    :ivar stem: The base name of the WSI file without extension.
    :type stem: str
    :ivar vendor: The vendor of the WSI, as defined in its properties.
    :type vendor: str
    :ivar level_count: The number of resolution levels available in the WSI.
    :type level_count: int
    :ivar dimensions: The dimensions of the base resolution level of the WSI as
        (width, height).
    :type dimensions: tuple[int, int]
    :ivar level_dimensions: A tuple containing the dimensions (width, height)
        of each resolution level.
    :type level_dimensions: tuple[tuple[int, int], ...]
    :ivar level_downsamples: A tuple specifying the downsample factors for each
        resolution level.
    :type level_downsamples: tuple[float, ...]
    :ivar mpp: The microns per pixel (pixel spacing), if available; otherwise 0.
    :type mpp: float
    :ivar mpp_x: The horizontal spacing in microns per pixel, if available;
        otherwise 0.
    :type mpp_x: float
    :ivar mpp_y: The vertical spacing in microns per pixel, if available;
        otherwise 0.
    :type mpp_y: float
    """
    def __init__(self, path: str) -> None:
        """
        Initializes a new instance of the class, resolving the given path,
        verifying its existence, and extracting properties from the file
        using OpenSlide.

        :param path: Path to the file to be processed
        :type path: str

        :raises TypeError: If the provided `path` is not a string.
        :raises FileNotFoundError: If the provided `path` does not exist.
        """
        if not isinstance(path, str):
            raise TypeError("Path must be a string.")
        wsi_path = Path(path).resolve()
        if not wsi_path.exists():
            raise FileNotFoundError("File not found.")
        self._path = wsi_path
        self._name = wsi_path.name
        self._stem = wsi_path.stem
        with OpenSlide(wsi_path) as slide:
            vendor = slide.properties.get("openslide.vendor")
            self._vendor = vendor if vendor is not None else "Unknown"
            self._level_count = slide.level_count
            self._dimensions = slide.dimensions
            self._level_dimensions = slide.level_dimensions
            self._level_downsamples = slide.level_downsamples
            mpp_y = slide.properties.get("openslide.mpp-y")
            mpp_x = slide.properties.get("openslide.mpp-x")
            self._mpp_y = float(mpp_y) if mpp_y is not None else float(0)
            self._mpp_x = float(mpp_x) if mpp_x is not None else float(0)
            if (self._mpp_x == self._mpp_y) and (self._mpp_x > 0):
                self._mpp = self._mpp_x
            else:
                self._mpp = float(0)

    def pixels_from_microns(self, microns: float, level: int) -> float:
        """
        Converts a distance in microns to pixels for a specified level of resolution.

        This method calculates the equivalent pixel value for a given micron distance
        considering the specified resolution level of the whole-slide image (WSI).
        The slide's microns-per-pixel (MPP) and level downsamples are taken into account
        to perform this conversion.

        :param microns: The distance in microns to be converted. Must be a positive float.
        :param level: The resolution level for which the conversion is performed.
                      This must be an integer greater than or equal to 0 and less than
                      the total number of levels (`self.level_count`).
        :return: The distance in pixels corresponding to the given micron distance at
                 the specified resolution level.
        :rtype: float

        :raises TypeError: If `microns` is not a float or convertible to float,
                           or if `level` is not an integer.
        :raises ValueError: If `microns` is non-positive, if `level` is out of the
                            valid range, or if the slide lacks pixel size information.
        """
        if isinstance(microns, int):
            microns = float(microns)
        if not isinstance(microns, float):
            raise TypeError("Microns must be a float.")
        if not isinstance(level, int):  raise TypeError("Level must be an integer.")
        if level < 0 or level >= self.level_count:
            raise ValueError(
                "Level must be greater than or equal to zero and less than the level count of the WSI."
            )
        if microns <= 0:
            raise ValueError("Microns must be greater than zero.")
        if self.mpp == 0:
            raise ValueError("WSI has no pixel size information.")
        return microns / (self.mpp * self.level_downsamples[level])

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
    def mpp(self) -> float:
        return self._mpp

    @property
    def mpp_x(self) -> float:
        return self._mpp_x

    @property
    def mpp_y(self) -> float:
        return self._mpp_y

    def __repr__(self) -> str:
        return f"<WSI: {self.name}>"
