from pydantic import BaseModel
from typing import Union, List

class User(BaseModel):
    id: Union[ int, None ] = None
    name: str
    lastname: str
    nickname: str
    password: str
    profile: int
    status: bool