from pydantic import BaseModel, EmailStr


class TokenPayload(BaseModel):
    ref: str
    email: EmailStr
