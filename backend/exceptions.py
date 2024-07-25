from fastapi import HTTPException

INCORRECT_LOGIN_DATA_EXCEPTION = HTTPException(
    status_code=400,
    detail="Неверные данные для входа."
)

INCORRECT_REGISTRATION_DATA_EXCEPTION = HTTPException(
    detail="Неверные данные для регистрации.",
    status_code=405,
)

USER_ALREADY_REGISTERED_EXCEPTION = HTTPException(
    detail="Данный пользователь уже зарегистрирован.",
    status_code=405,
)

PASSWORD_INVALID = HTTPException(
    detail="Неверный старый пароль!",
    status_code=400,
)
