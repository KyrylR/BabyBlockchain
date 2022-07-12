from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DigitalProduct:
    data: Optional[str] = field(default=None)
