from abc import ABC, abstractmethod

import numpy as np


class Module(ABC):
    """
    Abstract base class for a module responsible for certain operations.

    This class provides a framework for implementing specific modules with standardized methods.
    The purpose is to ensure that derived modules implement methods for fitting data,
    executing core functionality, and serialization/deserialization with configurations.

    :ivar name: The name of the module.
    :type name: str
    :ivar fitted: Indicates whether the module has been fitted or initialized.
    :type fitted: bool
    """

    def __init__(self, name: str) -> None:
        """
        Initialize the instance of the class.

        :param name: The name associated with the instance.
        :type name: str
        :raises TypeError: If the provided name is not a string.
        :raises ValueError: If the provided name is an empty string.
        """
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if len(name) == 0:
            raise ValueError("name must not be empty")
        self._name = name
        self._fitted = False

    @abstractmethod
    def fit(self, img_path: str, **kwargs) -> None:
        """
        Fits the model to the data from the given image path.
        This method must be implemented by any subclass inheriting
        from this abstract class. The details of how the model is
        fitted will depend on the specific implementation in the
        subclass.

        :param img_path: The file path to the image data used for
            fitting the model.
        :param kwargs: Additional arguments to customize the fitting
            process. The specific usage of these arguments depends
            on the concrete implementation.
        :return: This method does not return any value.
        """
        pass

    @abstractmethod
    def run(self, **kwargs) -> np.ndarray:
        """
        Abstract base method for defining the execution logic in subclasses.

        This method must be implemented by any subclass to provide specific
        execution functionality. The implementation should perform the intended
        operation based on the input parameters and return the result as a NumPy
        array.

        :param kwargs: Keyword arguments needed for the specific execution logic.
        :return: A NumPy array containing the result of the execution logic.
        """
        pass

    @staticmethod
    @abstractmethod
    def from_config(config: dict) -> "Module":
        """
        Creates an instance of a module from the configuration dictionary provided.

        The method is abstract and must be implemented by subclasses to define how
        the module instance should be created using the given configuration settings.

        :param config: A dictionary containing necessary configuration details
            required for initializing the module.
        :type config: dict
        :return: A module instance created from the given configuration dictionary.
        :rtype: Module
        """
        pass

    @abstractmethod
    def to_config(self) -> dict:
        """
        Converts the implementing object to its dictionary configuration representation.

        This method should be implemented by all subclasses to provide a structured
        dictionary representation of the object’s configuration. The dictionary
        is intended for serialization or similar purposes.

        :raises NotImplementedError: When the method is not implemented in a subclass.
        :return: A dictionary containing the configuration of the object.
        :rtype: dict
        """
        pass

    @property
    def name(self) -> str:
        """
        Provides access to the name attribute.

        This property allows retrieval of the name associated with this
        object. The name is returned as a string and reflects the value
        stored internally.

        :return: The name associated with the object.
        :rtype: str
        """
        return self._name

    @property
    def fitted(self) -> bool:
        """
        Indicates whether the object has been fitted.

        This property checks the private attribute `_fitted` to determine
        if a fitting process has been successfully completed.

        :rtype: bool
        :return: True if the object has been fitted, False otherwise.
        """
        return self._fitted
