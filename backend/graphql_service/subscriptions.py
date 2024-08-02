import asyncio

import graphene

import models

from . import exceptions, types
from .decorators import authorized_only
from .query import Query

DELAY = 1


class WorkspaceSubscription:
    """
    Подписка graphql для вывода данных рабочих пространств в реальном времени
    """

    workspace = graphene.Field(
        types.Workspace,
        workspace_id=graphene.NonNull(graphene.ID),
    )

    workspaces = graphene.Field(
        graphene.List(types.Workspace),
    )

    @staticmethod
    @authorized_only
    async def subscribe_workspace(_, __, user, workspace_id: str):
        while True:
            await asyncio.sleep(DELAY)
            workspace = await models.Workspace.objects.get_or_none(
                id=int(workspace_id),
                participants__user=user,
            )
            if not workspace:
                raise exceptions.WORKSPACE_NOT_FOUND
            yield workspace

    @staticmethod
    @authorized_only
    async def subscribe_workspaces(root, info, user):
        while True:
            await asyncio.sleep(DELAY)
            yield await Query.resolve_workspaces(root, info, user)


class CommentsSubscription:
    """
    Подписка graphql для вывода данных комментариев в реальном времени
    """

    comment = graphene.Field(
        types.Comment,
        comment_id=graphene.NonNull(graphene.ID),
    )

    comments = graphene.Field(
        graphene.List(types.Comment),
        task_id=graphene.NonNull(graphene.ID),
    )

    @staticmethod
    @authorized_only
    async def subscribe_comment(_, __, user, comment_id: int):
        while True:
            await asyncio.sleep(DELAY)
            comment = await models.Comment.objects.get_or_none(
                id=int(comment_id),
                task__group__board__workspace__participants__user=user,
            )
            if not comment:
                raise exceptions.COMMENT_NOT_FOUND

            yield comment

    @staticmethod
    @authorized_only
    async def subscribe_comments(root, info, user, task_id: int):
        while True:
            await asyncio.sleep(DELAY)
            yield await Query.resolve_comments(root, info, user, task_id)


class RoleSubscription:
    """
    Подписка graphql для вывода данных ролей в реальном времени
    """

    role = graphene.Field(
        types.Role,
        role_id=graphene.NonNull(graphene.ID),
    )

    roles = graphene.Field(
        graphene.List(types.Role),
        workspace_id=graphene.NonNull(graphene.ID),
    )

    @staticmethod
    @authorized_only
    async def subscribe_role(_, __, user, role_id: int):
        while True:
            await asyncio.sleep(DELAY)
            role = await models.Role.objects.get_or_none(
                id=int(role_id),
                workspace__participants__user=user,
            )

            if not role:
                raise exceptions.ROLE_NOT_FOUND

            yield role

    @staticmethod
    @authorized_only
    async def subscribe_roles(root, info, user, workspace_id: int):
        while True:
            await asyncio.sleep(DELAY)
            yield await Query.resolve_roles(root, info, user, workspace_id)


class TaskSubscription:
    """
    Подписка graphql для вывода данных задач в реальном времени
    """

    task = graphene.Field(
        types.Task,
        task_id=graphene.NonNull(graphene.ID),
    )

    tasks = graphene.Field(
        graphene.List(types.Task),
        board_id=graphene.NonNull(graphene.ID),
    )

    @staticmethod
    @authorized_only
    async def subscribe_task(_, __, user, task_id: int):
        while True:
            await asyncio.sleep(DELAY)
            task = await models.Task.objects.get_or_none(
                id=int(task_id),
                group__board__workspace__participants__user=user
            )

            if not task:
                message = "Запрашиваемая Вами задача не найдена."
                raise ValueError(message)

            yield task

    @staticmethod
    @authorized_only
    async def subscribe_tasks(root, info, user, board_id: int):
        while True:
            await asyncio.sleep(DELAY)
            yield await Query.resolve_tasks(root, info, user, board_id)


class BoardSubscription:
    """
    Подписка graphql для вывода данных досок задач в реальном времени
    """

    board = graphene.Field(
        types.Board,
        board_id=graphene.NonNull(graphene.ID),
    )

    boards = graphene.Field(
        graphene.List(types.Board),
        workspace_id=graphene.NonNull(graphene.ID),
    )

    @staticmethod
    @authorized_only
    async def subscribe_board(_, __, user, board_id: int):
        while True:
            await asyncio.sleep(DELAY)
            board = await models.Board.objects.get_or_none(
                id=int(board_id),
                workspace__participants__user=user,
            )

            if not board:
                raise exceptions.BOARD_NOT_FOUND

            yield board

    @staticmethod
    @authorized_only
    async def subscribe_boards(root, info, user, workspace_id: int):
        while True:
            await asyncio.sleep(DELAY)
            yield await Query.resolve_boards(root, info, user, workspace_id)


class PermissionSubscription:
    permissions = graphene.Field(
        graphene.List(types.IPermission),
        workspace_id=graphene.NonNull(graphene.ID),
    )

    @staticmethod
    @authorized_only
    async def subscribe_permissions(root, info, user, workspace_id: int):
        yield await Query.resolve_permissions(root, info, user, workspace_id)
