
from typing import Generic, TypeVar, Self
from collections import defaultdict

K = TypeVar('K')


class Polynomial(Generic[K]):
    """Class for a single variable polynomial over a field K"""

    def __init__(self, /, coef_dict: defaultdict[K, int], *, variable: str = 'x'):
        """Initialize with coefficient dictionary and variable"""
        self.coef_dict = coef_dict
        self.variable = variable

    @classmethod
    def from_str(cls, /, poly_str: str) -> Self:
        """
        Create a polynomial object from a string
        """

