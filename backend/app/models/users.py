import string
from typing import Optional
from pydantic import EmailStr, constr, validator
from app.models.core import CoreModel, IDModelMixin, DatetimeModelMixin
from app.models.token import AccessToken
from app.models.profiles import ProfilePublic

def validate_username(username: str) -> str:
    allowed = string.ascii_letters + string.digits + '-' + '_'
    assert all(char in allowed for char in username), 'Invalid characters in username'
    assert len(username) >= 3, 'Username must be at least 3 characters'
    return username

class UserBase(CoreModel):
    # name: Optional[str]
    # surname: Optional[str]
    email: Optional[EmailStr]
    
    username: Optional[str]
    # about: Optional[str]
    email_verified: bool = False
    is_active: bool = True
    is_superuser: bool = False
    # team_id: Optional[int]
    # role: Optional[UserRole] = 0

class UserCreate(CoreModel):
    email: EmailStr
    username: constr(min_length=3, regex='[a-zA-Z0-9_-]+$')
    password: constr(min_length=7, max_length=100)

class UserUpdate(CoreModel):
    email: Optional[EmailStr]
    username: Optional[constr(min_length=3, regex='[a-zA-Z0-9_-]+$')]
    # role: Optional[UserRole]

class UserPasswordUpdate(CoreModel):
    password: constr(min_length=7, max_length=100)
    salt: str

class UserInDB(IDModelMixin, DatetimeModelMixin, UserBase):
    password: constr(min_length=7, max_length=100)
    salt: str
    profile: Optional[ProfilePublic]

class UserPublic(IDModelMixin, DatetimeModelMixin, UserBase):
    access_token: Optional[AccessToken]
    profile: Optional[ProfilePublic]
