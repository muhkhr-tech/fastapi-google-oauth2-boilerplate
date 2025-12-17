from pydantic import BaseModel

class UserSchema(BaseModel):
    email: str
    name: str

class UserProlieSchema(UserSchema):
    pass