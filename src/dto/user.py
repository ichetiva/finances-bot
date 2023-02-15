from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int

    class Config:
        orm_mode = True
