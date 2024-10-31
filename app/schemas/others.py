from pydantic import BaseModel, EmailStr


class TokenPayload(BaseModel):
    ref: str
    email: EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
