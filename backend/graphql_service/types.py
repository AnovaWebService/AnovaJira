import graphene
import graphene_pydantic

import models


class OrmarMixin:

    @classmethod
    def from_ormar(cls, instance):
        values = {}

        for key, value in cls.__dict__.items():
            if not key or key.startswith("_"):
                continue

            field = value.__dict__["_type"]
            if isinstance(field, graphene.NonNull):
                field = field.__dict__.get("_of_type", field)

            field_meta = field._meta.__dict__  # noqa: SLF001
            field_class_type = field_meta.get("class_type")
            if field_meta.get("fields") and field_class_type and issubclass(field_class_type, OrmarMixin):
                values[key] = field_meta.get("class_type").from_ormar(getattr(instance, key))
                continue

            if hasattr(instance, key):
                values[key] = getattr(instance, key)

        return cls(**values) # noqa


class Permission(OrmarMixin, graphene.ObjectType):
    """
    Модель разрешения
    """

    id = graphene.Field(graphene.Int())
    code = graphene.Field(graphene.String())


class IPermission(OrmarMixin, graphene_pydantic.PydanticObjectType):
    """
    Модель разрешения на объект
    """

    permission = graphene.Field(Permission)

    class Meta:
        model = models.IPermission.get_pydantic(
            include={
                "id",
                "instance_class",
                "instance_id",
            }
        )


class User(OrmarMixin, graphene_pydantic.PydanticObjectType):
    """
    Модель пользователя graphql
    """

    class Meta:
        model = models.User.get_pydantic(
            include={
                "id",
                "username",
                "avatar",
                "password",
                "email",
                "first_name",
                "last_name",
                "email_verified",
                "date_joined",
            }
        )


class Workspace(OrmarMixin, graphene.ObjectType):
    """
    Модель для чтения данных рабочего пространства graphql_service
    """

    id = graphene.Field(graphene.ID)
    title = graphene.Field(graphene.String)


class WorkspaceCreate(graphene.InputObjectType):
    """
    Модель для создания и редактирования рабочего пространства graphql_service
    """

    title = graphene.InputField(graphene.String())


class WorkspaceUpdate(graphene.InputObjectType):
    """
    Модель для редактирования рабочего пространства
    """

    id = graphene.InputField(graphene.ID, required=True)
    title = graphene.InputField(graphene.String, required=True)


class Role(OrmarMixin, graphene_pydantic.PydanticObjectType):
    """
    Модель роли рабочего пространства graphql_service
    """

    permissions = graphene.Field(graphene.List(IPermission))
    workspace = graphene.Field(Workspace)

    class Meta:
        model = models.Role.get_pydantic(
            include={
                "id",
                "name",
                "for_user",
            }
        )


class RoleInput(graphene_pydantic.PydanticInputObjectType):
    """
    Модель для создания и редактирования роли рабочего пространства
    """

    permissions = graphene.Field(graphene.List(IPermission))

    class Meta:
        model = models.Role.get_pydantic(
            exclude={
                "id",
                "workspace",
            }
        )


class Participant(OrmarMixin, graphene.ObjectType):
    """
    Модель участника рабочего пространства
    """

    workspace = graphene.Field(Workspace)
    user = graphene.Field(User)
    role = graphene.Field(Role)


class Board(OrmarMixin, graphene.ObjectType):
    """
    Модель доски задачи graphql_service
    """

    id = graphene.Field(
        graphene.ID
    )
    name = graphene.Field(
        graphene.NonNull(graphene.String)
    )
    slug_ticker = graphene.Field(
        graphene.NonNull(graphene.String)
    )
    workspace = graphene.Field(Workspace)


class BoardCreate(graphene.InputObjectType):
    """
    Модель для создания и редактирования досок задач
    """

    workspace_id = graphene.InputField(
        graphene.NonNull(graphene.ID)
    )
    name = graphene.InputField(
        graphene.NonNull(graphene.String)
    )
    slug_ticker = graphene.InputField(
        graphene.NonNull(graphene.String)
    )


class BoardUpdate(graphene.InputObjectType):
    """
    Модель для редактирования доски задач
    """

    board_id = graphene.InputField(
        graphene.NonNull(graphene.ID)
    )
    name = graphene.InputField(
        graphene.NonNull(graphene.String)
    )
    slug_ticker = graphene.InputField(
        graphene.NonNull(graphene.String)
    )


class TaskGroup(OrmarMixin, graphene_pydantic.PydanticObjectType):
    """
    Модель группы задач доски
    """

    board = graphene.Field(Board)

    class Meta:
        model = models.TaskGroup.get_pydantic(
            include={
                "id",
                "title",
                "color",
            }
        )


class Task(OrmarMixin, graphene_pydantic.PydanticObjectType):
    """
    Модель задачи graphql
    """

    assigners = graphene.Field(
        graphene.List(Participant)
    )
    group = graphene.Field(TaskGroup)
    creator = graphene.Field(Participant)

    class Meta:
        model = models.Task.get_pydantic(
            include={
                "id",
                "slug",
                "title",
                "description",
                "branch",
                "date_created",
                "date_ending",
            }
        )


class Comment(OrmarMixin, graphene_pydantic.PydanticObjectType):
    """
    Модель комментария задачи graphql_service
    """

    creator = graphene.Field(Participant)
    task = graphene.Field(Task)

    class Meta:
        model = models.Comment.get_pydantic(
            include={
                "id",
                "text",
                "status",
                "date_created",
                "date_modified",
            }
        )


class CommentInput(graphene_pydantic.PydanticInputObjectType):
    """
    Модель для создания и редактирования комментариев к задачам.
    """

    class Meta:
        model = models.Comment.get_pydantic(
            exclude={
                "id",
                "task",
                "creator",
            }
        )


class TaskInput(graphene_pydantic.PydanticInputObjectType):
    """
    Модель для создания и редактирования задач.
    """

    class Meta:
        model = models.Task.get_pydantic(
            exclude={
                "id",
                "slug",
                "creator",
                "date_created",
            }
        )
