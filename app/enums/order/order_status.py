from enum import Enum


class OrderStatus(Enum):
    NEW = 'new'
    PAID = 'paid'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'