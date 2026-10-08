from dataclasses import dataclass


@dataclass
class CategoryDataDto:
    id: int | None
    name: str
