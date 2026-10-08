from decimal import Decimal
from typing import Annotated

from pydantic import PlainSerializer


def decimal_to_float(value: Decimal) -> float:
    return float(value)


Price = Annotated[
    Decimal,
    PlainSerializer(
        float,
        return_type=float,
        when_used='json',
    ),
]
