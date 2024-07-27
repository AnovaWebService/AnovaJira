import enum
import typing
import urllib.request
from datetime import datetime

import databases
import ormar
import sqlalchemy

import mixins
import settings
import utils

database = databases.Database(settings.DATABASE_URL)
engine = sqlalchemy.create_engine(settings.DATABASE_URL)
metadata = sqlalchemy.MetaData(bind=engine)

ormar_config = ormar.OrmarConfig(
    database=database,
    metadata=metadata,
)


async def get_user_default_avatar():
    random_seed = datetime.now().timestamp()
    url = f"https://api.dicebear.com/7.x/miniavs/svg?seed={random_seed}"

    image_save_path, rel_path = utils.get_avatar_save_path(f"{random_seed}.svg")

    urllib.request.urlretrieve(  # noqa: S310
        url=url,
        filename=image_save_path,
    )

    return rel_path


class IdentifiedMixin:
    id = ormar.BigInteger(
        nullable=False,
        primary_key=True,
        autoincrement=True,
        minimum=1,
    )


class CommentStatuses(enum.Enum):
    OPEN = 1
    COMPLETED = 2
    CLOSED = 3


class Permission(IdentifiedMixin, ormar.Model):
    """
    Модель разрешения
    """

    ormar_config = ormar_config.copy(
        tablename="permissions",
    )

    code = ormar.String(
        max_length=30,
        nullable=False,
        unique=True,
    )

    instance_class = ormar.String(
        max_length=50,
        nullable=False,
    )


class IPermission(IdentifiedMixin, ormar.Model):
    """
    Модель разрешения на конкретный объект бд.
    """

    ormar_config = ormar_config.copy(
        tablename="i_permissions",
    )

    permission = ormar.ForeignKey(
        to=Permission,
        nullable=False,
        on_delete=ormar.ReferentialAction.CASCADE,
        on_update=ormar.ReferentialAction.CASCADE,
        related_name="instance_permissions",
    )

    instance_id = ormar.BigInteger(
        nullable=True,
        minimum=1,
    )


class ResolvableMixin:
    """
    Mixin для наделения модели правами доступа.
    """

    permissions = ormar.ManyToMany(
        to=IPermission,
        unique=True,
    )


class PermissionTargetMixin(IdentifiedMixin):
    """
    Mixin для добавления функционала прав доступа
    """

    @classmethod
    async def _get_permission(cls, code: str):
        return await Permission.objects.get(
            code=code,
        )

    @classmethod
    async def give_global_permission(
        cls,
        resolvable: ResolvableMixin,
        permission_code: str,
    ):
        permission = await cls._get_permission(permission_code)

        model_permission, _ = await IPermission.objects.get_or_create(
            permission=permission,
            instance_id__isnull=True,
        )

        await resolvable.permissions.add(model_permission)

    @classmethod
    async def remove_global_permission(
        cls,
        resolvable: ResolvableMixin,
        permission_code: str,
    ):
        permission = await IPermission.objects.get_or_none(
            permission__code=permission_code,
            permission__instance_name=cls.__name__,
            instance_id__isnull=True,
        )

        if not permission:
            return None

        return await resolvable.permissions.remove(permission, keep_reversed=True)

    async def give_permission(
        self,
        resolvable: ResolvableMixin,
        permission_code: str,
    ):
        permission = await self._get_permission(permission_code)

        object_permission, _ = await IPermission.objects.get_or_create(
            permission=permission,
            instance_id=self.id,
        )

        await resolvable.permissions.add(object_permission)

    async def check_permission(
        self,
        resolvable: ResolvableMixin,
        permission_code: str,
    ):
        return await resolvable.permissions.filter(
            permission__code=permission_code,
            permission__instance_name=self.__class__.__name__,
            instance_id=self.id,
        ).exists() or await resolvable.permissions.filter(
            permission__code=permission_code,
            permission__instance_name=self.__class__.__name__,
            instance_id__isnull=True,
        ).exists()

    async def remove_permission(
        self,
        resolvable: ResolvableMixin,
        permission_code: str,
    ):
        instance_permission = await IPermission.objects.get_or_none(
            permission__code=permission_code,
            permission__instance_name=self.__class__.__name__,
            instance_id=self.id,
        )

        if not instance_permission:
            return None

        return await resolvable.permissions.remove(instance_permission, keep_reversed=True)


class User(mixins.PartialMixin, ormar.Model):
    """
    Модель пользователя БД
    """

    ormar_config = ormar_config.copy(
        tablename="users",
    )

    id = ormar.Integer(
        autoincrement=True,
        primary_key=True,
        nullable=False,
        minimum=1,
    )

    username = ormar.String(
        max_length=100,
        nullable=False,
    )

    avatar = ormar.Text(
        nullable=False,
        default=get_user_default_avatar,
    )

    password = ormar.Text(
        nullable=False,
    )

    email = ormar.Text(
        regex=r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$",
        nullable=False,
    )

    first_name = ormar.String(
        max_length=100,
        nullable=False,
    )

    last_name = ormar.String(
        max_length=100,
        nullable=True,
    )

    email_verified = ormar.Boolean(
        default=False,
        nullable=False,
    )

    date_joined = ormar.DateTime(
        timezone=True,
        default=datetime.now,
    )


class Workspace(
    mixins.PartialMixin,
    PermissionTargetMixin,
    ormar.Model,
):
    """
    Модель рабочего пространства БД
    Разрешения:
        update_workspace,
        create_boards,
        setup_color_theme,
        setup_background_image,
        invite_participants,
        manage_invitations,
        manage_roles,
        kick_participants,
    """

    ormar_config = ormar_config.copy(
        tablename="workspaces",
    )

    id = ormar.BigInteger(
        autoincrement=True,
        primary_key=True,
        nullable=False,
        minimum=1,
    )

    title = ormar.String(
        max_length=100,
        nullable=False
    )

    permissions: typing.ClassVar = [
        "update_workspace",
        "create_boards",
        "invite_participants",
        "manage_invitations",
        "manage_roles",
        "kick_participants",
    ]


class Board(
    mixins.PartialMixin,
    PermissionTargetMixin,
    ormar.Model,
):
    """
    Модель доски задач рабочего пространства БД
    Разрешения:
        update_boards,
        delete_boards,
        manage_participants,
        remove_tasks,
        create_tasks,
        update_tasks,
        delete_groups,
        create_groups,
        update_groups,
        leave_comments,
        manage_comments,
        delete_foreign_comments,
        update_foreign_comments,
    """

    ormar_config = ormar_config.copy(
        tablename="boards",
    )

    workspace = ormar.ForeignKey(
        to=Workspace,
        nullable=False,
        on_delete=ormar.ReferentialAction.CASCADE,
        on_update=ormar.ReferentialAction.CASCADE,
        related_name="boards",
    )

    name = ormar.String(
        max_length=50,
        nullable=False,
    )

    slug_ticker = ormar.String(
        max_length=10,
        nullable=False,
        default="TASK"
    )

    permissions: typing.ClassVar = [
        "update_boards",
        "delete_boards",
        "manage_participants",
        "remove_tasks",
        "create_tasks",
        "update_tasks",
        "delete_groups",
        "create_groups",
        "update_groups",
        "leave_comments",
        "manage_comments",
        "delete_foreign_comments",
        "update_foreign_comments",
    ]


class TaskGroup(
    IdentifiedMixin,
    mixins.PartialMixin,
    ormar.Model,
):
    """
    Модель списка задач
    """

    ormar_config = ormar_config.copy(
        tablename="t_groups",
    )

    title = ormar.String(
        max_length=50,
        nullable=False,
    )

    color = ormar.String(
        max_length=7,
        nullable=True,
        regex=r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
    )

    board = ormar.ForeignKey(
        to=Board,
        nullable=False,
        on_delete=ormar.ReferentialAction.CASCADE,
        on_update=ormar.ReferentialAction.CASCADE,
        related_name="groups"
    )


class Role(
    mixins.PartialMixin,
    PermissionTargetMixin,
    ResolvableMixin,
    ormar.Model
):
    """
    Модель роли рабочего пространства
    """

    ormar_config = ormar_config.copy(
        tablename="roles",
    )

    id = ormar.BigInteger(
        autoincrement=True,
        primary_key=True,
        nullable=False,
        minimum=1,
    )

    name = ormar.String(
        max_length=50,
        nullable=False,
    )

    workspace = ormar.ForeignKey(
        to=Workspace,
        nullable=False,
        on_delete=ormar.ReferentialAction.CASCADE,
        on_update=ormar.ReferentialAction.CASCADE,
        related_name="roles",
    )

    for_user = ormar.Boolean(
        default=False,
        nullable=False,
    )


class Participant(
    IdentifiedMixin,
    mixins.PartialMixin,
    ormar.Model,
):
    """
    Связующая модель пользователя с ролью
    """

    ormar_config = ormar_config.copy(
        tablename="participants",
    )

    workspace = ormar.ForeignKey(
        to=Workspace,
        nullable=False,
        on_delete=ormar.ReferentialAction.CASCADE,
        on_update=ormar.ReferentialAction.CASCADE,
        related_name="participants",
    )

    user = ormar.ForeignKey(
        to=User,
        nullable=False,
        on_delete=ormar.ReferentialAction.CASCADE,
        on_update=ormar.ReferentialAction.CASCADE,
        related_name="participants",
    )

    role = ormar.ForeignKey(
        to=Role,
        nullable=False,
        on_delete=ormar.ReferentialAction.RESTRICT,
        on_update=ormar.ReferentialAction.CASCADE,
        related_name="participants",
    )

    @classmethod
    async def get_for_workspace(cls, workspace, user):
        return await cls.objects.get_or_none(
            workspace=workspace,
            user=user
        )


class Task(
    IdentifiedMixin,
    mixins.PartialMixin,
    ormar.Model,
):
    """
    Модель задачи БД
    """

    ormar_config = ormar_config.copy(
        tablename="tasks",
    )

    slug = ormar.String(
        max_length=50,
        nullable=True,
    )

    title = ormar.String(
        max_length=100,
        nullable=False,
    )

    description = ormar.Text(
        nullable=True,
    )

    branch = ormar.String(
        max_length=50,
        nullable=True,
    )

    assigners = ormar.ManyToMany(
        to=Participant,
        unique=True,
        related_name="tasks"
    )

    creator = ormar.ForeignKey(
        to=Participant,
        nullable=False,
        on_delete=ormar.ReferentialAction.CASCADE,
        on_update=ormar.ReferentialAction.CASCADE,
        related_name="created_tasks",
    )

    group = ormar.ForeignKey(
        to=TaskGroup,
        nullable=False,
        on_delete=ormar.ReferentialAction.CASCADE,
        on_update=ormar.ReferentialAction.CASCADE,
        related_name="tasks",
    )

    date_created = ormar.DateTime(
        default=datetime.now,
        timezone=True,
        nullable=False,
    )

    date_ending = ormar.DateTime(
        nullable=True,
        timezone=True,
    )


class Comment(
    IdentifiedMixin,
    mixins.PartialMixin,
    ormar.Model,
):
    """
    Модель комментария задачи
    """

    ormar_config = ormar_config.copy(
        tablename="comments",
    )

    creator = ormar.ForeignKey(
        to=Participant,
        nullable=False,
        on_delete=ormar.ReferentialAction.CASCADE,
        on_update=ormar.ReferentialAction.CASCADE,
        related_name="comments",
    )

    text = ormar.Text(
        nullable=False,
    )

    status = ormar.String(
        max_length=50,
        choices=list(CommentStatuses),
        nullable=False,
        default=CommentStatuses.OPEN.value,
    )

    task = ormar.ForeignKey(
        to=Task,
        nullable=False,
        on_delete=ormar.ReferentialAction.CASCADE,
        on_update=ormar.ReferentialAction.CASCADE,
        related_name="comments",
    )

    date_created = ormar.DateTime(
        default=datetime.now,
        timezone=True,
        nullable=False,
    )

    date_modified = ormar.DateTime(
        nullable=True,
        timezone=True,
    )
