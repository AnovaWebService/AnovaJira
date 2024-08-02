import pydantic

import models

UserRegistrationSerializer = models.User.get_pydantic(
    include={
        "email",
        "first_name",
        "last_name",
        "password",
    }
)


class UserPasswordChangeSerializer(pydantic.BaseModel):
    old_password: str
    new_password: str


UserUpdateSerializer = models.User.get_pydantic_partial(
    include={
        "email",
        "first_name",
        "last_name",
    }
)
