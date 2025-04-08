from typing import TypedDict

class UserValidationData(TypedDict):
    username: str
    email: str
    password: str
    password2: str
    is_active: bool
    is_staff: bool
    is_superuser: bool