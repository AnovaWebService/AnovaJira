import graphene

import models

from . import exceptions, types
from .decorators import authorized_only


class WorkspaceCreateMutation(graphene.Mutation):
    """
    Мутация для создания рабочего пространства
    """

    class Arguments:
        data = types.WorkspaceCreate()

    Output = types.Workspace

    @staticmethod
    @authorized_only
    async def mutate(_, __, user, data: dict):
        workspace = await models.Workspace.objects.create(
            **data
        )

        role = await models.Role.objects.get(
            name="Супер-админ",
            workspace=workspace,
            for_user=False,
        )

        await models.Participant.objects.create(
            workspace=workspace,
            user=user,
            role=role,
        )

        return types.Workspace.from_ormar(workspace)


class WorkspaceUpdateMutation(graphene.Mutation):
    """
    Мутация для редактирования рабочего пространства
    """

    class Arguments:
        data = types.WorkspaceUpdate()

    Output = types.Workspace

    @staticmethod
    @authorized_only
    async def mutate(_, __, user, data: types.WorkspaceUpdate):
        workspace_id = int(data.id)

        workspace: models.Workspace = await models.Workspace.objects.get_or_none(
            id=workspace_id
        )

        if not workspace:
            raise exceptions.WORKSPACE_NOT_FOUND

        workspace_user = await models.Participant.get_for_workspace(
            workspace=workspace,
            user=user,
        )

        if not workspace_user:
            raise exceptions.WORKSPACE_NOT_A_PARTICIPANT

        if not workspace.check_permission(
            workspace_user.role,
            "update_workspace"
        ):
            raise exceptions.WORKSPACE_UPDATE_NOT_PERMITTED

        await workspace.update(
            title=data.title
        )

        return types.Workspace.from_ormar(workspace)


class BoardCreateMutation(graphene.Mutation):
    class Arguments:
        data = types.BoardCreate()

    Output = types.Board

    @staticmethod
    @authorized_only
    async def mutate(_, __, user, data: types.BoardCreate):
        workspace = await models.Workspace.objects.get_or_none(
            id=int(data.workspace_id)
        )

        if not workspace:
            raise exceptions.WORKSPACE_NOT_FOUND

        participant = await models.Participant.get_for_workspace(workspace, user)
        if not participant:
            raise exceptions.WORKSPACE_NOT_A_PARTICIPANT

        if not await workspace.check_permission(participant.role, "create_board"):
            raise exceptions.WORKSPACE_BOARD_CREATE_NOT_PERMITTED

        board, is_created = await models.Board.objects.get_or_create(
            name=data.name,
            workspace=workspace,
            _defaults={
                "workspace": workspace,
                "slug_ticker": data.slug_ticker,
            }
        )

        if not is_created:
            raise exceptions.BOARD_ALREADY_EXISTS

        await board.give_permission(participant.role, "update_board")
        await board.give_permission(participant.role, "delete_board")
        await board.give_permission(participant.role, "view_board")

        return types.Board.from_ormar(board)


class BoardUpdateMutation(graphene.Mutation):
    class Arguments:
        data = types.BoardUpdate()

    Output = types.Board

    @staticmethod
    @authorized_only
    async def mutate(_, __, user, data: types.BoardUpdate):
        board_id = int(data.board_id)

        board = await models.Board.objects.select_related("workspace").get_or_none(
            id=board_id
        )

        if not board:
            raise exceptions.BOARD_NOT_FOUND

        participant = await models.Participant.get_for_workspace(board.workspace, user)
        if not board.check_permission(participant.role, "remove_board"):
            raise exceptions.BOARD_UPDATE_NOT_PERMITTED

        await board.update(
            name=data.name,
            slug_ticker=data.slug_ticker,
        )

        return types.Board.from_ormar(board)


class BoardDeleteMutation(graphene.Mutation):
    class Arguments:
        board_id = graphene.Argument(
            graphene.NonNull(graphene.ID)
        )

    Output = types.Board

    @staticmethod
    @authorized_only
    async def mutate(_, __, user, board_id: int):
        board: models.Board = await models.Board.objects.get_or_none(
            id=board_id
        )

        if not board:
            raise exceptions.BOARD_NOT_FOUND

        participant = await models.Participant.get_for_workspace(board.workspace, user)
        if not board.check_permission(participant.role, "remove_board"):
            raise exceptions.BOARD_DELETE_NOT_PERMITTED

        await board.delete()

        return types.Board.from_ormar(board)
