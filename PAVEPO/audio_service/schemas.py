from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    yandex_id: str

class UserOut(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True

class AudioBase(BaseModel):
    filename: str

class AudioCreate(AudioBase):
    pass

class AudioOut(AudioBase):
    id: int
    filepath: str

    class Config:
        from_attributes = True