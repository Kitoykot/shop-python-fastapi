from sqlalchemy.orm import Session


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session