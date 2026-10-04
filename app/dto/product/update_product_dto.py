from dataclasses import dataclass
from typing import Any


@dataclass
class UpdateProductDto:
    fields: dict[str, Any]
