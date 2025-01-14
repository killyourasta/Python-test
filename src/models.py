from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    name: str
    surname: str
    age: int


class UserModel(BaseModel):
    id: int
    name: str
    surname: str
    age: int

    class Config:
        orm_mode = True


class PicnicRegistrationModel(BaseModel):
    id: int
    user_surname: str
    picnic_id: int
