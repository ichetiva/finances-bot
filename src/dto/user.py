from pydantic import BaseModel

from .wallet import WalletDTO


class UserDTO(BaseModel):
    id: int
    wallets: list[WalletDTO]

    class Config:
        orm_mode = True
