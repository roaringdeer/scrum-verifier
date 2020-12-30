import random, string
from typing import Tuple
from fastapi import Depends, HTTPException, status
from app.api.dependencies.users import get_current_active_user
from app.models.users import UserInDB

async def get_stream_key(
    current_user: UserInDB = Depends(get_current_active_user),
) -> str:
    return ''.join((random.choice(string.ascii_letters+string.digits) for i in range(10)))
