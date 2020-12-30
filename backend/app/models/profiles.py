from typing import Optional
from pydantic import EmailStr, constr, HttpUrl
from app.models.core import DatetimeModelMixin, IDModelMixin, CoreModel

class ProfileBase(CoreModel):
    full_name: Optional[str]
    phone_number: Optional[constr(regex='^\+?[0-9\s]+$')]
    bio: Optional[str]
    # image: Optional[HttpUrl]
    image: Optional[str]

class ProfileCreate(ProfileBase):
    user_id: int

class ProfileUpdate(ProfileBase):
    pass

class ProfileInDB(ProfileBase, IDModelMixin, DatetimeModelMixin):
    user_id: int
    username: Optional[str]
    email: Optional[EmailStr]

class ProfilePublic(ProfileInDB):
    pass