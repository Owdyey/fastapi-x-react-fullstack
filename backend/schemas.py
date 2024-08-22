from pydantic import BaseModel, conint


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

    model_config = {
        "from_attributes" : True
    }


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None  = None


class ItemCreate(BaseModel):
    name: str
    description: str
    price: int

    model_config ={
        "from_attributes": True
    }

class Item(ItemCreate):
    id: int