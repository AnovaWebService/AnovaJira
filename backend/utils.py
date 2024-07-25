import os

import settings


def get_relpath(path: os.PathLike | str):
    return os.path.relpath(path, settings.BASE_DIR)


def get_avatar_save_path(file_name: str):
    save_path = settings.MEDIA_ROOT / "avatars" / file_name

    return (
        save_path,
        get_relpath(save_path)
    )
