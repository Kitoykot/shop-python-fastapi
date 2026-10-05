from enum import Enum


class OrderStatus(Enum):
    NEW = 'new'
    PAID = 'paid'
    CANCELLED = 'cancelled'
    IN_TRANSIT = 'in_transit'
    COMPLETED = 'completed'

    @property
    def label(self) -> str:
        match self:
            case OrderStatus.NEW:
                return 'Новый'
            case OrderStatus.PAID:
                return 'Оплачен'
            case OrderStatus.CANCELLED:
                return 'Отменен'
            case OrderStatus.IN_TRANSIT:
                return 'В пути'
            case OrderStatus.COMPLETED:
                return 'Выполнен'
            