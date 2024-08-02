import os
import pathlib
from collections.abc import Iterable, Mapping

import settings


def get_relpath(path: os.PathLike | str):
    return os.path.relpath(path, settings.BASE_DIR)


def get_avatar_save_path(file_name: str):
    save_path = settings.MEDIA_ROOT / "avatars" / file_name

    return (
        save_path,
        get_relpath(save_path)
    )


def remove_file(file_path: str, missing_ok: bool = True):  # noqa: FBT001, FBT002
    pathlib.Path(settings.BASE_DIR / file_path).unlink(missing_ok)


def get_attr_chain(attribute: str, data: object):
    attribute_list = None

    if not attribute:
        return None

    if "__" in attribute:
        attribute_list = attribute.split("__")

    if attribute_list:
        return get_attr_chain(
            "__".join(attribute_list[1:]),
            getattr(data, attribute_list[0])
        )

    return getattr(data, attribute)


def group_by_attr(attribute: str, data_iterable: Iterable[Mapping | object]):
    """
    Функция группировки списка с вложенными словарями или другими Mapping объектами.
    :param attribute: Аттрибут, по которому будет производиться группировка
    :param data_iterable: Список данных для группировки.
    :return: Сгруппированные данные.
    """
    data = {}

    for item in data_iterable:
        data_key = get_attr_chain(attribute, item)

        if data_key not in data:
            data[data_key] = [item]
            continue

        data[data_key].append(item)

    return data
