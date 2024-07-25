import enum
import urllib.request
from datetime import datetime

import databases
import ormar
import sqlalchemy
from sqlalchemy_utils import create_database, database_exists

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
    Модель разрешения на рабочее пространство или доску задач
    """

    ormar_config = ormar_config.copy(
        tablename="permissions",
    )

    instance_class = ormar.String(
        max_length=50,
        nullable=False,
    )

    instance_id = ormar.BigInteger(
        nullable=True,
        minimum=1,
    )

    code = ormar.String(
        max_length=20,
        nullable=False,
    )


class ResolvableMixin:
    """
    Mixin для наделения модели правами доступа.
    """

    permissions = ormar.ManyToMany(
        to=Permission,
        unique=True,
    )


class PermissionTargetMixin(IdentifiedMixin):
    """
    Mixin для добавления функционала прав доступа
    """

    @classmethod
    async def give_global_permission(
        cls,
        resolvable: ResolvableMixin,
        permission_code: str,
    ):
        model_permission, is_created = await Permission.objects.get_or_create(
            code=permission_code,
            instance_id=None,
            instance_name=cls.__name__,
        )

        await resolvable.permissions.add(model_permission)

    @classmethod
    async def remove_global_permission(
        cls,
        resolvable: ResolvableMixin,
        permission_code: str,
    ):
        return await resolvable.permissions.delete(
            each=True,
            permissions__name=permission_code,
            instance_name=cls.__name__,
            instance_id__isnull=True,
        )

    async def give_permission(
        self,
        resolvable: ResolvableMixin,
        permission_code: str,
    ):
        object_permission, is_created = await Permission.objects.get_or_create(
            code=permission_code,
            instance_id=self.id,
            instance_name=self.__class__.__name__,
        )

        await resolvable.permissions.add(object_permission)

    async def check_permission(
        self,
        resolvable: ResolvableMixin,
        permission_code: str,
    ):
        return await resolvable.permissions.filter(
            permissions__name=permission_code,
            instance_name=self.__class__.__name__,
            instance_id=self.id,
        ).exists() or resolvable.permissions.filter(
            permissions__name=permission_code,
            instance_name=self.__class__.__name__,
            instance_id__isnull=True,
        )

    async def remove_permission(
        self,
        resolvable: ResolvableMixin,
        permission_code: str,
    ):
        return await resolvable.permissions.delete(
            each=True,
            permissions__name=permission_code,
            instance_name=self.__class__.__name__,
            instance_id=self.id,
        )


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
        encrypt_secret=settings.SECRET_KEY,
        encrypt_backend=ormar.EncryptBackends.HASH,
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


class Board(
    mixins.PartialMixin,
    PermissionTargetMixin,
    ormar.Model,
):
    """
    Модель доски задач рабочего пространства БД
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


class TaskGroup(
    IdentifiedMixin,
    mixins.PartialMixin,
    ormar.Model,
):
    """
    Модель списка задач
    """

    ormar_config = ormar_config.copy(
        tablename="board_groups",
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

    workspace = ormar.ForeignKey(
        to=Workspace,
        nullable=False,
        on_delete=ormar.ReferentialAction.CASCADE,
        on_update=ormar.ReferentialAction.CASCADE,
    )

    board = ormar.ForeignKey(
        to=Board,
        nullable=False,
        on_delete=ormar.ReferentialAction.CASCADE,
        on_update=ormar.ReferentialAction.CASCADE,
    )


class WorkspaceRole(
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


class WorkspaceUser(
    IdentifiedMixin,
    mixins.PartialMixin,
    ormar.Model,
):
    """
    Связующая модель пользователя с ролью
    """

    ormar_config = ormar_config.copy(
        tablename="workspace_users",
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
        related_name="workspace_users",
    )

    role = ormar.ForeignKey(
        to=WorkspaceRole,
        nullable=False,
        on_delete=ormar.ReferentialAction.RESTRICT,
        on_update=ormar.ReferentialAction.CASCADE,
        related_name="workspace_users",
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

    id = ormar.BigInteger(
        nullable=True,
        primary_key=True,
        autoincrement=True,
        minimum=1,
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
        to=WorkspaceUser,
        unique=True,
        related_name="tasks"
    )

    creator = ormar.ForeignKey(
        to=WorkspaceUser,
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
        to=WorkspaceUser,
        nullable=False,
        on_delete=ormar.ReferentialAction.CASCADE,
        on_update=ormar.ReferentialAction.CASCADE,
        related_name="comments",
    )

    text = ormar.Text(
        nullable=False,
    )

    status = ormar.Enum(
        enum_class=CommentStatuses,
        nullable=False,
        default=CommentStatuses.OPEN,
    )

    task = ormar.ForeignKey(
        to=Task,
        nullable=False,
        on_delete=ormar.ReferentialAction.CASCADE,
        on_update=ormar.ReferentialAction.CASCADE,
        related_name="comments",
    )
