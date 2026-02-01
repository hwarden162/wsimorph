import numpy as np
from openslide import OpenSlide

from ..image._tile import Tile
from ..image._wsi import WSI


def read_tile(
    wsi: WSI,
    level: int,
    y_start: int,
    x_start: int,
    y_len: int,
    x_len: int,
    padding: int,
) -> Tile:
    """
    Reads a specific region or tile from a whole slide image (WSI) at a specified level of resolution.

    Validates input parameters to ensure the coordinates, dimensions, and padding are appropriate
    for the given level in the WSI. The function extracts, normalizes, and returns the requested
    tile along with metadata such as padding and starting positions.

    :param wsi: The whole slide image (WSI) instance to extract the tile from.
    :type wsi: WSI
    :param level: The level of resolution within the WSI to read the tile from.
    :type level: int
    :param y_start: The Y-coordinate of the tile's starting position in the specified level.
    :type y_start: int
    :param x_start: The X-coordinate of the tile's starting position in the specified level.
    :type x_start: int
    :param y_len: The height of the region to read in pixels.
    :type y_len: int
    :param x_len: The width of the region to read in pixels.
    :type x_len: int
    :param padding: Additional padding (in pixels) to add around the tile, if possible.
    :type padding: int
    :return: A Tile object containing the image data, metadata about the region, and padding details.
    :rtype: Tile
    :raises TypeError: If any input argument has an incorrect type.
    :raises ValueError: If coordinate/dimension values are out of bounds or invalid for the WSI level.
    :raises NotImplementedError: If the image data type in the WSI is not supported.
    """
    if not isinstance(wsi, WSI):
        raise TypeError("wsi must be a WSI object.")
    if not isinstance(level, int):
        raise TypeError("level must be an integer.")
    if level < 0 or level >= wsi.level_count:
        raise ValueError(
            "level must be greater than or equal to zero and less than the level count of the WSI."
        )
    level_dimensions = wsi.level_dimensions[level]
    if not isinstance(y_start, int) or not isinstance(x_start, int):
        raise TypeError("y_start and x_start must be integers.")
    if y_start < 0 or x_start < 0:
        raise ValueError("y_start and x_start must be non-negative.")
    if not isinstance(y_len, int) or not isinstance(x_len, int):
        raise TypeError("y_len and x_len must be integers.")
    if y_len <= 0 or x_len <= 0:
        raise ValueError("y_len and x_len must be positive.")
    if y_start + y_len > level_dimensions[0] or x_start + x_len > level_dimensions[1]:
        raise ValueError(
            "y_start + y_len exceeds the level dimensions or x_start + x_len exceeds the level dimensions."
        )
    if not isinstance(padding, int):
        raise TypeError("padding must be an integer.")
    if padding < 0:
        raise ValueError("padding must be non-negative.")
    y_start_tile = max(0, y_start - padding)
    x_start_tile = max(0, x_start - padding)
    y_end_tile = min(level_dimensions[0], y_start + y_len + padding)
    x_end_tile = min(level_dimensions[1], x_start + x_len + padding)
    y_len_tile = y_end_tile - y_start_tile
    x_len_tile = x_end_tile - x_start_tile
    ylo_pad = y_start - y_start_tile
    yhi_pad = y_end_tile - y_start - y_len
    xlo_pad = x_start - x_start_tile
    xhi_pad = x_end_tile - x_start - x_len
    with OpenSlide(wsi.path) as slide:
        image = np.array(
            slide.read_region(
                (x_start_tile, y_start_tile), level, (x_len_tile, y_len_tile)
            ).convert("RGB")
        )
    if np.isdtype(image.dtype, np.uint8):
        tile_image = image.astype(np.float32) / 255.0
    elif np.isdtype(image.dtype, np.uint16):
        tile_image = image.astype(np.float32) / 65535.0
    else:
        raise NotImplementedError("Image data type not supported.")
    return Tile(
        tile_image,
        y_start_tile,
        x_start_tile,
        level,
        ylo_pad,
        yhi_pad,
        xlo_pad,
        xhi_pad,
        wsi,
    )
