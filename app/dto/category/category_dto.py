from dataclasses import dataclass


@dataclass
class CategoryDto:
    id: int | None
    name: str
