from auth import get_current_user

from . import exceptions


def authorized_only(func):
    async def wrapper(root, info, *args, **kwargs):
        headers = {
            key.decode("utf-8"): value.decode("utf-8")
            for key, value in dict(info.context.get("request", {}).get("headers", {})).items()
        }

        auth_header = headers.get("Authorization", "")
        if not auth_header:
            raise exceptions.NOT_AUTHORIZED

        auth_token = auth_header.split(" ")[1]
        current_user = get_current_user(auth_token)

        return await func(root, info, current_user, *args, **kwargs)

    return wrapper


