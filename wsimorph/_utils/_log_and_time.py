# type: ignore

import logging
import time
from functools import wraps
from typing import Any, Callable

from humanize.time import precisedelta


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("WSIMorph")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)

    return logger


WSIMORPH_CLI_LOGGER = setup_logger()


def log_and_time(message: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    if not isinstance(message, str):
        raise TypeError("Message must be a string.")

    def decorator(func) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start = time.time()
            WSIMORPH_CLI_LOGGER.info(f"[STARTED] {message}")
            result = func(*args, **kwargs)
            end = time.time()
            elapsed = end - start
            print_time = precisedelta(
                elapsed, minimum_unit="milliseconds" if elapsed < 1 else "seconds"
            )
            WSIMORPH_CLI_LOGGER.info(f"[COMPLETED] {message} in {print_time}.")
            wrapper.elapsed_time = elapsed
            return result

        return wrapper

    return decorator
