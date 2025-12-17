import logging
import time
from functools import wraps
from typing import Any, Callable

from humanize.time import precisedelta


def setup_logger():
    """
    Sets up and configures a logger named "WSIM" with a specified logging level and format.
    The logger will log messages to the console using a stream handler with a custom format.
    If the logger already has handlers, the setup avoids adding duplicate handlers.

    :returns: Configured logger instance
    :rtype: logging.Logger
    """
    logger = logging.getLogger("WSIM")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)

    return logger


WSIM_CLI_LOGGER = setup_logger()


def log_and_time(message: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Returns a decorator that logs the execution time of a function and outputs a start and completion message
    using a logger.

    This function generates a decorator that wraps a given function with logic to log the start and completion
    time of its execution. The log message includes a custom message provided during the creation of the decorator
    and the precise duration in either microseconds or seconds.

    :param message: A string message to include in the log statements. It describes the purpose or context of the
                    decorated function.
    :type message: str

    :return: A decorator function that wraps another function to log its execution time.
    :rtype: Callable[[Callable[..., Any]], Callable[..., Any]]

    :raises TypeError: If the `message` argument is not of type `str`.
    """
    if not isinstance(message, str):
        raise TypeError("Message must be a string.")

    def decorator(func) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start = time.time()
            WSIM_CLI_LOGGER.info(f"[STARTED] {message}")
            result = func(*args, **kwargs)
            end = time.time()
            elapsed = end - start
            print_time = precisedelta(
                elapsed, minimum_unit="milliseconds" if elapsed < 1 else "seconds"
            )
            WSIM_CLI_LOGGER.info(f"[COMPLETED] {message} in {print_time}.")
            wrapper.elapsed_time = elapsed
            return result

        return wrapper

    return decorator