from datetime import datetime, timedelta
from pydantic import EmailStr
from app.core.config import JWT_AUDIENCE, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.core import CoreModel

class JWTMeta(CoreModel):
    #Issuer of the token
    iss: str = 'scrum-verifier.io'
    #who this token is intended for
    aud: str = JWT_AUDIENCE
    #when this token was issued
    iat: float = datetime.timestamp(datetime.now())
    #when this token expires
    exp: float = datetime.timestamp(datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

class JWTCreds(CoreModel):
    sub: EmailStr
    username: str

class JWTPayload(JWTMeta, JWTCreds):
    pass

class AccessToken(CoreModel):
    access_token: str
    token_type: str