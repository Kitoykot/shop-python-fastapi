from dataclasses import dataclass


@dataclass
class OrderStatusDto:
    code: str
    label: str
