from typing import Optional

import pydantic


class PartialMixin:
    """
    Mixin для создания сериализаторов без обязательных полей
    для возможности обновления данных без валидации.
    """

    @classmethod
    def get_pydantic_partial(
            cls,
            *,
            include: set | dict | None = None,
            exclude: set | dict | None = None,
    ) -> type[pydantic.BaseModel]:
        model = cls.get_pydantic(include=include, exclude=exclude)

        new_fields = {
            name: (Optional[model.__annotations__.get(name)], None)  # noqa: UP007
            for name in model.__fields__
        }

        return pydantic.create_model(f"Partial{cls.__name__}", **new_fields)


