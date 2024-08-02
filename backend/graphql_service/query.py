import graphene

import models

from . import exceptions, types
from .decorators import authorized_only


class Query(graphene.ObjectType):
    """
    Все доступные запросы
    """

    workspaces = graphene.List(types.Workspace)
    roles = graphene.List(types.Role, workspace_id=graphene.ID())
    boards = graphene.List(types.Board, workspace_id=graphene.ID())
    comments = graphene.List(types.Board, task_id=graphene.ID())
    tasks = graphene.List(types.Board, board_id=graphene.ID())
    participants = graphene.List(types.Participant, workspace_id=graphene.ID())
    permissions = graphene.List(types.IPermission, workspace_id=graphene.ID())

    @staticmethod
    @authorized_only
    async def resolve_workspaces(_, __, user):
        return await models.Workspace.objects.filter(
            participants__user=user,
        ).all()

    @staticmethod
    @authorized_only
    async def resolve_roles(_, __, user, workspace_id: int):
        return await models.Role.objects.select_related([
            "workspace",
            "permissions",
        ]).filter(
            workspace__id=int(workspace_id),
            workspace__participants__user=user,
        ).all()

    @staticmethod
    @authorized_only
    async def resolve_boards(_, __, user, workspace_id: int):
        return await models.Board.objects.filter(
            workspace__id=int(workspace_id),
            workspace__participants__user=user,
        ).all()

    @staticmethod
    @authorized_only
    async def resolve_comments(_, __, user, task_id: int):
        return await models.Comment.objects.filter(
            task__id=int(task_id),
            task__group__board__workspace__participants__user=user,
        ).all()

    @staticmethod
    @authorized_only
    async def resolve_tasks(_, __, user, board_id: int):
        return await models.Task.objects.filter(
            group__board__id=int(board_id),
            group__board__workspace__participants__user=user,
        ).all()

    @staticmethod
    @authorized_only
    async def resolve_participants(_, __, user, workspace_id: int):
        return await models.Participant.objects.select_related([
            "role",
            "workspace",
            "user",
        ]).filter(
            workspace__id=int(workspace_id),
            workspace__participants__user=user,
        ).all()

    @staticmethod
    @authorized_only
    async def resolve_permissions(_, __, user, workspace_id: int):
        workspace = await models.Workspace.objects.get_or_none(
            id=int(workspace_id),
        )
        if not workspace:
            raise exceptions.WORKSPACE_NOT_FOUND

        participant = await models.Participant.get_for_workspace(workspace, user)
        if not participant:
            raise exceptions.WORKSPACE_NOT_A_PARTICIPANT

        return await participant.role.permissions.select_related("permission").all()
