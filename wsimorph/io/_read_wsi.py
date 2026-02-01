from pathlib import Path

from .._utils._log_and_time import log_and_time # type: ignore[attr-defined]
from ..image._wsi import WSI


@log_and_time("reading WSI")
def read_wsi(path: Path | str) -> WSI:
    """
    Reads a Whole Slide Image (WSI) from a specified file path.

    This function takes a file path, either as a string or a
    ``pathlib.Path`` object, and returns a ``WSI`` object. It
    ensures the input is a valid path, converting string paths
    to ``pathlib.Path`` if necessary. If the input is not a
    string or ``pathlib.Path``, it raises a ``TypeError``.

    :param path: The file system path to the WSI file. Can be provided
        as a string or a ``pathlib.Path`` object.
    :type path: Path | str
    :return: A ``WSI`` object loaded from the provided file path.
    :rtype: WSI
    """
    if isinstance(path, str):
        path = Path(path)
    if not isinstance(path, Path):
        raise TypeError("Path must be a string or pathlib.Path object.")
    return WSI(path)
