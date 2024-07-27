import ormar

import models

roles = {
    "Участник": {
        "create_tasks",
        "update_tasks",
        "leave_comments",
    },
    "Модератор": {
        "create_tasks",
        "update_tasks",
        "leave_comments",
        "manage_invitations",
        "manage_comments",
        "delete_foreign_comments",
        "update_foreign_comments",
    },
    "Администратор": {
        "create_tasks",
        "update_tasks",
        "leave_comments",
        "manage_invitations",
        "manage_comments",
        "delete_foreign_comments",
        "update_foreign_comments",
        "create_groups",
        "update_groups",
        "delete_groups",
        "create_boards",
        "update_boards",
        "delete_boards",
    },
    "Супер-админ": {
        "create_tasks",
        "update_tasks",
        "leave_comments",
        "manage_comments",
        "delete_foreign_comments",
        "update_foreign_comments",
        "create_groups",
        "update_groups",
        "delete_groups",
        "create_boards",
        "update_boards",
        "delete_boards",
        "update_workspace",
        "invite_participants",
        "manage_invitations",
        "manage_roles",
        "kick_participants",
    }

}


@ormar.pre_update(models.User)
async def reset_user_email_confirmation(sender, instance: models.User, **kwargs):  # noqa: ARG001
    """
    Сбрасывает флаг email_verified, если почта пользователя была изменена.
    """
    if "email" not in kwargs:
        return

    instance.email_verified = False


@ormar.post_save(models.Workspace)
async def initialize_workspace_permissions(sender, instance: models.Workspace, **kwargs):  # noqa: ARG001
    for role, permissions in roles.items():
        role_created = await models.Role.objects.create(
            name=role,
            workspace=instance,
            permissions=[
                await models.IPermission.objects.create(
                    permission=(
                        await models.Permission.objects.get(
                            code=code
                        )
                    ),
                    instance_id=None,
                ) for code in permissions
            ]
        )
        print(role_created, sep='\n\n')


@ormar.post_save(models.Task)
async def generate_task_id(_, instance: models.Task, **kwargs):  # noqa: ARG001
    ticker_count = await models.Task.objects.filter(
        group__board__workspace__id=instance.group.board.workspace.id,
    ).count() or 0 + 1

    ticker_string = instance.group.board.slug_ticker

    instance.slug = f"{ticker_string}-{ticker_count}"


