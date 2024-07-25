import ormar

import models

ALL_WORKSPACE_PERMISSIONS = [
    "boards__create_board",
    "workspace__setup_user_theme",
    "workspace__invite_people",
    "workspace__kick_people",
    "workspace__manage_roles",
    "workspace__"
]

DEFAULT_USER_PERMISSIONS = [
    "boards__create_board",
    "boards__update_board",
    "boards__delete_board",
    "boards__update_workspace",
    "workspace__setup_user_theme",
    "workspace__invite_people",
    "workspace__kick_people"
]


@ormar.pre_update(models.User)
async def reset_user_email_confirmation(_, instance: models.User, **kwargs):
    """
    Сбрасывает флаг email_verified, если почта пользователя была изменена.
    """
    if "email" not in kwargs:
        return

    instance.email_verified = False


@ormar.post_save(models.Workspace)
async def initialize_workspace_permissions(_, instance: models.Workspace):
    await models.WorkspaceRole.objects.create(
        name="Участник",
        workspace=instance
    )


@ormar.post_save(models.Task)
async def generate_task_id(_, instance: models.Task):
    ticker_count = await models.Task.objects.filter(
        group__board__workspace__id=instance.group.board.workspace.id,
    ).count() or 0 + 1

    ticker_string = instance.group.board.slug_ticker

    instance.slug = f"{ticker_string}-{ticker_count}"


