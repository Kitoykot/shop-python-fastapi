from pydantic import BaseModel


class PaymentConfirmedResponse(BaseModel):
    code: int
    message: str
