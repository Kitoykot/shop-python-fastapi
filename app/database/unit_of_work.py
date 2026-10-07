from sqlalchemy.orm import Session


class UnitOfWork:
    def __init__(self, session: Session):
        self.session = session

    def __enter__(self) -> UnitOfWork:
        return self

    # exc_type - вид exception
    # exc_value - его объект
    # traceback - трейс (где случилось исключение)
    # проверка на None exc_type достаточна только для типа
    # если всё ок, то код выполняется дальше и транзакция применяется
    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        if exc_type is not None:
            self.session.rollback()
            return False

        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

        return False
