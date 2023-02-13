from pydantic import BaseModel


class WalletDTO(BaseModel):
    id: int
    user_id: int
    name: str
    balance: float
    currency: str

    class Config:
        orm_mode = True
