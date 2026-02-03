import numpy as np
from skimage.filters import gaussian

from ..process import ABCProcess
from ...image import Tile


class GaussianBlur(ABCProcess):

    def __init__(self, sigma: float, units: str = "micron") -> None:
        super().__init__("GaussianBlur")
        if isinstance(sigma, int):
            sigma = float(sigma)
        if not isinstance(sigma, float):
            raise TypeError("Sigma must be a float.")
        if not isinstance(units, str):
            raise TypeError("Units must be a string.")
        if not units.lower() in ["micron", "pixel"]:
            raise ValueError("Units must be either 'micron' or 'pixel'.")
        self._sigma = sigma
        self._units = units.lower()

    def run(self, tile: Tile) -> Tile:
        if not isinstance(tile, Tile):
            raise TypeError("Tile must be a Tile object.")
        if self._units == "micron":
            if tile.parent_wsi.mpp == 0:
                raise ValueError("WSI has no pixel size information.")
            sigma = tile.parent_wsi.pixels_from_microns(self._sigma, tile.level)
        else:
            sigma = self._sigma
        new_image = gaussian(tile.image, sigma=[sigma, sigma, 0])
        return Tile(new_image, tile.y_start, tile.x_start, tile.level, tile.ylo_pad, tile.yhi_pad, tile.xlo_pad, tile.xhi_pad, tile.parent_wsi)

    @staticmethod
    def from_config(self, config: dict) -> "GaussianBlur":
        if not isinstance(config, dict):
            raise TypeError("Config must be a dictionary.")
        if not "sigma" in config:
            raise KeyError("Config dictionary is missing the 'sigma' key.")
        if not "units" in config:
            raise KeyError("Config dictionary is missing the 'units' key.")
        return GaussianBlur(config["sigma"], config["units"])

    def to_config(self) -> dict:
        config = {
            "name": self.name,
            "sigma": self._sigma,
            "units": self._units
        }
        return config
