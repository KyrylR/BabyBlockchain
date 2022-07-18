from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DigitalProduct:
    # Some string data
    __data: Optional[str] = field(default=None)

    @property
    def get_data(self):
        """
        Get digital data.
        :return: data.
        """
        return self.__data
