from dataclasses import dataclass


@dataclass
class PaginationDto:
    page: int
    per_page: int
    total: int
    pages: int
