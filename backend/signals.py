import datetime

import ormar

import auth
import models
import settings
import utils

roles = {
    "Участник": {
        "create_tasks",
        "update_tasks",
        "leave_comments",
    },
    "Модератор": {
        "view_board",
        "create_tasks",
        "update_tasks",
        "delete_tasks",
        "leave_comments",
        "manage_invitations",
        "manage_comments",
        "delete_foreign_comments",
        "update_foreign_comments",
    },
    "Администратор": {
        "create_tasks",
        "update_tasks",
        "delete_tasks",
        "reassign_tasks",
        "leave_comments",
        "manage_invitations",
        "manage_comments",
        "manage_board_participants",
        "delete_foreign_comments",
        "update_foreign_comments",
        "create_groups",
        "update_groups",
        "delete_groups",
        "create_boards",
        "update_board",
        "delete_board",
    },
    "Супер-админ": {
        "create_tasks",
        "update_tasks",
        "delete_tasks",
        "reassign_tasks",
        "leave_comments",
        "manage_comments",
        "manage_board_participants",
        "delete_foreign_comments",
        "update_foreign_comments",
        "create_groups",
        "update_groups",
        "delete_groups",
        "create_boards",
        "update_board",
        "delete_board",
        "update_workspace",
        "invite_participants",
        "manage_invitations",
        "manage_roles",
        "kick_participants",
    }

}


@ormar.pre_save(models.User)
async def set_user_password_hash(sender, instance, **kwargs):  # noqa: ARG001
    """
    Шифрует поле пароля пользователя перед добавлением объекта в БД
    """
    password = kwargs.get("password", "")
    if not password:
        return

    password = auth.create_password_hash(password)
    await instance.update(
        password=password
    )


@ormar.post_delete(models.User)
async def delete_local_user_avatar(sender, instance: models.User, **kwargs):  # noqa: ARG001
    """
    Сигнал, удаляющий файл аватара пользователя при удалении самого пользователя.
    P.S. Почему-то удаляет файлы только после выключения сервера, мне лень разбираться почему.
    """
    utils.remove_file(instance.avatar)


@ormar.pre_update(models.User)
async def delete_old_local_avatar(sender, instance: models.User, **kwargs):  # noqa: ARG001
    """
    Удаляет файл старого аватара пользователя, если аватар меняется на новый.
    """
    if "avatar" not in kwargs:
        return

    utils.remove_file(instance.avatar)

    await instance.update(
        avatar=kwargs.get("avatar"),
    )


@ormar.pre_update(models.User)
async def reset_user_email_confirmation(sender, instance: models.User, passed_args: dict, **kwargs):  # noqa: ARG001
    """
    Сбрасывает флаг email_verified, если почта пользователя была изменена.
    """
    if "email" not in passed_args:
        return

    await instance.update(
        email_verified=False
    )


@ormar.post_save(models.Workspace)
async def initialize_workspace_permissions(sender, instance: models.Workspace, **kwargs):  # noqa: ARG001
    for role, permissions in roles.items():
        role_created = await models.Role.objects.create(
            name=role,
            workspace=instance,
        )

        for permission in permissions:
            await role_created.permissions.add(
                await models.IPermission.objects.create(
                    permission=(
                        await models.Permission.objects.get(
                            code=permission
                        )
                    )
                )
            )


@ormar.pre_save(models.Task)
async def generate_task_id(_, instance: models.Task, **kwargs):  # noqa: ARG001
    ticker_count = await models.Task.objects.filter(
        group__board__workspace__id=instance.group.board.workspace.id,
    ).count() or 0 + 1

    ticker_string = instance.group.board.slug_ticker

    await instance.update(
        slug=f"{ticker_string}-{ticker_count}"
    )


@ormar.pre_delete(models.Board)
async def clear_board_permissions(sender, instance: models.Board, **kwargs):  # noqa: ARG001
    permissions = await models.IPermission.get_for_instance(instance)
    await permissions.delete(each=True)


@ormar.pre_delete(models.Workspace)
async def clear_workspace_permissions(sender, instance: models.Workspace, **kwargs):  # noqa: ARG001
    permissions = await models.IPermission.get_for_instance(instance)
    await permissions.delete(each=True)


@ormar.pre_update(models.Comment)
async def set_comment_date_modified(sender, instance: models.Comment, **kwargs):  # noqa: ARG001
    await instance.update(
        date_modified=datetime.datetime.now(tz=settings.TIMEZONE),
    )
