from datetime import datetime

from pydantic import BaseModel


class TransactionDTO(BaseModel):
    id: int
    wallet_id: int
    amount: float
    currency: str
    comment: str | None
    created_at: datetime

    class Config:
        orm_mode = True
