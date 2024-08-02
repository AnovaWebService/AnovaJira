import graphene

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

    id = graphene.Field(graphene.Int)
    code = graphene.Field(graphene.String)


class IPermission(OrmarMixin, graphene.ObjectType):
    """
    Модель разрешения на объект
    """

    id = graphene.Field(
        graphene.ID
    )
    permission = graphene.Field(
        Permission
    )
    instance_id = graphene.Field(
        graphene.ID
    )


class User(OrmarMixin, graphene.ObjectType):
    """
    Модель пользователя graphql
    """

    id = graphene.Field(graphene.ID)
    avatar = graphene.Field(graphene.String)
    password = graphene.Field(graphene.String)
    email = graphene.Field(graphene.String)
    first_name = graphene.Field(graphene.String)
    last_name = graphene.Field(graphene.String)
    email_verified = graphene.Field(graphene.Boolean)
    date_joined = graphene.Field(
        graphene.DateTime
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


class Role(OrmarMixin, graphene.ObjectType):
    """
    Модель роли рабочего пространства graphql_service
    """

    id = graphene.Field(
        graphene.NonNull(graphene.ID)
    )
    name = graphene.Field(
        graphene.NonNull(graphene.String)
    )
    for_user = graphene.Field(
        graphene.Boolean
    )
    permissions = graphene.Field(
        graphene.List(IPermission)
    )
    workspace = graphene.Field(
        Workspace
    )


class RoleInput(graphene.InputObjectType):
    """
    Модель для создания и редактирования роли рабочего пространства
    """

    name = graphene.Field(
        graphene.NonNull(graphene.String)
    )
    for_user = graphene.Field(
        graphene.Boolean
    )
    permissions = graphene.Field(
        graphene.List(IPermission)
    )


class Participant(OrmarMixin, graphene.ObjectType):
    """
    Модель участника рабочего пространства
    """

    id = graphene.Field(graphene.ID)
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


class TaskGroup(OrmarMixin, graphene.ObjectType):
    """
    Модель группы задач доски
    """

    id = graphene.Field(
        graphene.NonNull(graphene.ID)
    )
    title = graphene.Field(
        graphene.NonNull(graphene.String)
    )
    color = graphene.Field(
        graphene.NonNull(graphene.String)
    )
    board = graphene.Field(Board)


class TaskGroupCreate(graphene.InputObjectType):
    title = graphene.Field(
        graphene.NonNull(graphene.String)
    )
    color = graphene.Field(
        graphene.NonNull(graphene.String)
    )
    board_id = graphene.Field(
        graphene.NonNull(graphene.ID)
    )


class TaskGroupUpdate(graphene.InputObjectType):
    id = graphene.Field(
        graphene.NonNull(graphene.ID)
    )
    title = graphene.Field(
        graphene.NonNull(graphene.String)
    )
    color = graphene.Field(
        graphene.NonNull(graphene.String)
    )


class Task(OrmarMixin, graphene.ObjectType):
    """
    Модель задачи graphql
    """

    id = graphene.Field(
        graphene.NonNull(graphene.ID)
    )
    slug = graphene.Field(
        graphene.NonNull(graphene.String)
    )
    title = graphene.Field(
        graphene.NonNull(graphene.String)
    )
    description = graphene.Field(
        graphene.String
    )
    branch = graphene.Field(
        graphene.String
    )
    date_created = graphene.Field(
        graphene.NonNull(graphene.DateTime)
    )
    date_ending = graphene.Field(
        graphene.DateTime
    )
    assigners = graphene.Field(
        graphene.List(Participant)
    )
    group = graphene.Field(
        graphene.NonNull(TaskGroup)
    )
    creator = graphene.Field(
        graphene.NonNull(Participant)
    )


class Comment(OrmarMixin, graphene.ObjectType):
    """
    Модель комментария к задачам graphql
    """

    id = graphene.Field(
        graphene.NonNull(graphene.ID)
    )
    text = graphene.Field(
        graphene.NonNull(graphene.String)
    )
    status = graphene.Field(
        graphene.NonNull(graphene.Int)
    )
    date_created = graphene.Field(
        graphene.NonNull(graphene.DateTime)
    )
    date_modified = graphene.Field(
        graphene.DateTime
    )
    creator = graphene.Field(
        graphene.NonNull(Participant)
    )
    task = graphene.Field(
        graphene.NonNull(Task)
    )


class CommentCreate(graphene.InputObjectType):
    """
    Модель для создания комментариев к задачам.
    """

    text = graphene.Field(
        graphene.NonNull(graphene.String)
    )

    task_id = graphene.Field(
        graphene.NonNull(graphene.ID)
    )


class CommentUpdate(graphene.InputObjectType):
    """
    Модель для редактирования комментариев к задачам.
    """

    id = graphene.Field(
        graphene.NonNull(graphene.ID)
    )
    text = graphene.Field(
        graphene.NonNull(graphene.String)
    )


class CommentManage(graphene.InputObjectType):
    """
    Модель для редактирования комментариев к задачам.
    """

    id = graphene.Field(
        graphene.NonNull(graphene.ID)
    )
    status = graphene.Field(
        graphene.NonNull(graphene.Int)
    )


class TaskCreate(graphene.InputObjectType):
    """
    Модель для создания и редактирования задач.
    """

    title = graphene.InputField(
        graphene.NonNull(graphene.String)
    )

    description = graphene.InputField(
        graphene.String
    )

    branch = graphene.InputField(
        graphene.String
    )

    assigners_id = graphene.InputField(
        graphene.List(graphene.ID)
    )

    group_id = graphene.InputField(
        graphene.NonNull(graphene.ID)
    )

    date_ending = graphene.InputField(
        graphene.DateTime
    )


class TaskUpdate(TaskCreate):
    """
    Модель для редактирования задачи
    """

    id = graphene.InputField(
        graphene.NonNull(graphene.ID)
    )
