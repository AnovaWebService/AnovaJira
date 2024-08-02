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

        if not await workspace.check_permission(
            workspace_user.role,
            "update_workspace"
        ):
            raise exceptions.WORKSPACE_UPDATE_NOT_PERMITTED

        await workspace.update(
            title=data.title
        )

        return types.Workspace.from_ormar(workspace)


class BoardCreateMutation(graphene.Mutation):
    """
    Мутация graphql для создания досок задач
    """

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

        if not await workspace.check_permission(participant.role, "create_boards"):
            raise exceptions.WORKSPACE_BOARD_CREATE_NOT_PERMITTED

        board, is_created = await models.Board.objects.get_or_create(
            name=data.name,
            workspace=workspace,
            _defaults={
                "slug_ticker": data.slug_ticker,
            }
        )

        if not is_created:
            raise exceptions.BOARD_ALREADY_EXISTS

        await board.give_permission(participant.role, "view_board")

        return types.Board.from_ormar(board)


class BoardUpdateMutation(graphene.Mutation):
    """
    Мутация graphql для редактирования досок задач
    """

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
        if not participant:
            raise exceptions.WORKSPACE_NOT_A_PARTICIPANT

        if not await board.check_permission(participant.role, "view_board"):
            raise exceptions.BOARD_VIEW_NOT_PERMITTED

        if not await board.check_permission(participant.role, "update_board"):
            raise exceptions.BOARD_UPDATE_NOT_PERMITTED

        await board.update(
            name=data.name,
            slug_ticker=data.slug_ticker,
        )

        return types.Board.from_ormar(board)


class BoardDeleteMutation(graphene.Mutation):
    """
    Мутация graphql для удаления досок задач
    """

    class Arguments:
        board_id = graphene.Argument(
            graphene.NonNull(graphene.ID)
        )

    Output = types.Board

    @staticmethod
    @authorized_only
    async def mutate(_, __, user, board_id: int):
        board: models.Board = await models.Board.objects.get_or_none(
            id=int(board_id)
        )

        if not board:
            raise exceptions.BOARD_NOT_FOUND

        participant = await models.Participant.get_for_workspace(board.workspace, user)
        if not participant:
            raise exceptions.WORKSPACE_NOT_A_PARTICIPANT

        if not await board.check_permission(participant.role, "view_board"):
            raise exceptions.BOARD_VIEW_NOT_PERMITTED

        if not await board.check_permission(participant.role, "delete_board"):
            raise exceptions.BOARD_DELETE_NOT_PERMITTED

        await board.delete()

        return types.Board.from_ormar(board)


class TaskCreateMutation(graphene.Mutation):
    """
    Мутация graphql для создания задач
    """

    class Arguments:
        data = types.TaskCreate()

    Output = types.Task

    @staticmethod
    @authorized_only
    async def mutate(_, __, user, data: types.TaskCreate):
        group = await models.TaskGroup.objects.get_or_none(
            id=int(data.group_id)
        )

        if not group:
            raise exceptions.TASK_GROUP_NOT_FOUND

        board: models.Board = group.board
        workspace: models.Workspace = board.workspace
        participant: models.Participant = await models.Participant.get_for_workspace(workspace, user)
        if not participant:
            raise exceptions.WORKSPACE_NOT_A_PARTICIPANT

        if not await board.check_permission(participant.role, "view_board"):
            raise exceptions.BOARD_VIEW_NOT_PERMITTED

        if not await board.check_permission(participant.role, "create_tasks"):
            raise exceptions.TASK_GROUP_CREATE_NOT_PERMITTED

        assigners = await workspace.participants.filter(
            id__in=data.assigners_id
        ).all()

        new_task = await models.Task.objects.create(
            title=data.title,
            description=data.description,
            date_ending=data.date_ending,
            branch=data.branch,
            creator=participant,
        )

        for assigner in assigners:
            await new_task.assigners.add(assigner)

        return types.Task.from_ormar(new_task)


class TaskUpdateMutation(graphene.Mutation):
    """
    Мутация graphql для редактирования задач
    """

    class Arguments:
        data = types.TaskUpdate()

    Output = types.Task

    @staticmethod
    @authorized_only
    async def mutate(_, __, user, data: types.TaskUpdate):
        task = await models.Task.objects.get_or_none(
            id=int(data.id)
        )

        if not task:
            raise exceptions.TASK_NOT_FOUND

        board: models.Board = task.group.board
        workspace: models.Workspace = board.workspace
        participant: models.Participant = await models.Participant.get_for_workspace(workspace, user)
        if not participant:
            raise exceptions.WORKSPACE_NOT_A_PARTICIPANT

        if not await board.check_permission(participant.role, "view_board"):
            raise exceptions.BOARD_VIEW_NOT_PERMITTED

        if not await board.check_permission(participant.role, "update_tasks"):
            raise exceptions.TASK_UPDATE_NOT_PERMITTED

        assigners = await workspace.participants.filter(
            id__in=data.assigners_id,
        ).all()

        if assigners != task.assigners and not await board.check_permission(participant.role, "reassign_tasks"):
            raise exceptions.TASK_ASSIGN_NOT_PERMITTED

        await task.assigners.clear()

        for assigner in assigners:
            await task.assigners.add(assigner)

        await task.update(
            title=data.title,
            description=data.description,
            date_ending=data.date_ending,
            branch=data.branch,
        )

        return types.Task.from_ormar(task)


class TaskGroupCreateMutation(graphene.Mutation):
    """
    Мутация graphql для создания списка задач внутри доски задач
    """

    class Arguments:
        data = types.TaskGroupCreate()

    Output = types.TaskGroup

    @staticmethod
    @authorized_only
    async def mutate(_, __, user, data: types.TaskGroupCreate):
        board: models.Board = await models.Board.objects.get_or_none(
            id=int(data.board_id)
        )

        if not board:
            raise exceptions.BOARD_NOT_FOUND

        workspace: models.Workspace = board.workspace
        participant = await models.Participant.get_for_workspace(workspace, user)
        if not participant:
            raise exceptions.WORKSPACE_NOT_A_PARTICIPANT

        if not await board.check_permission(participant.role, "view_board"):
            raise exceptions.BOARD_VIEW_NOT_PERMITTED

        if not await board.check_permission(participant.role, "create_groups"):
            raise exceptions.TASK_GROUP_CREATE_NOT_PERMITTED

        group, is_created = await models.TaskGroup.objects.get_or_create(
            title=data.title,
            board=board,
            _defaults={
                "color": data.color
            }
        )

        if not is_created:
            raise exceptions.TASK_GROUP_ALREADY_EXISTS

        return types.TaskGroup.from_ormar(group)


class TaskGroupUpdateMutation(graphene.Mutation):
    """
    Мутация graphql для редактирования списка задач внутри доски задач
    """

    class Arguments:
        data = types.TaskGroupUpdate()

    Output = types.TaskGroup

    @staticmethod
    @authorized_only
    async def mutate(_, __, user, data: types.TaskGroupUpdate):
        group: models.TaskGroup = await models.TaskGroup.objects.get_or_none(
            id=int(data.id)
        )

        if not group:
            raise exceptions.TASK_GROUP_NOT_FOUND

        board: models.Board = group.board
        workspace: models.Workspace = board.workspace

        participant = await models.Participant.get_for_workspace(workspace, user)
        if not participant:
            raise exceptions.WORKSPACE_NOT_A_PARTICIPANT

        if not await board.check_permission(participant.role, "view_board"):
            raise exceptions.BOARD_VIEW_NOT_PERMITTED

        if not await board.check_permission(participant.role, "update_groups"):
            raise exceptions.TASK_GROUP_UPDATE_NOT_PERMITTED

        await group.update(
            title=data.title,
            color=data.color,
        )

        return types.TaskGroup.from_ormar(group)


class TaskGroupDeleteMutation(graphene.Mutation):
    """
    Мутация graphql для удаления списка задач из доски задач
    """

    class Arguments:
        task_id = graphene.Argument(
            graphene.NonNull(graphene.ID)
        )

    Output = types.Task

    @staticmethod
    @authorized_only
    async def mutate(_, __, user, task_id: str):
        group: models.TaskGroup = await models.TaskGroup.objects.get_or_none(
            id=int(task_id)
        )

        if not group:
            raise exceptions.TASK_GROUP_NOT_FOUND

        board: models.Board = group.board
        workspace: models.Workspace = board.workspace

        participant = await models.Participant.get_for_workspace(workspace, user)
        if not participant:
            raise exceptions.WORKSPACE_NOT_A_PARTICIPANT

        if not await board.check_permission(participant.role, "view_board"):
            raise exceptions.BOARD_VIEW_NOT_PERMITTED

        if not await board.check_permission(participant.role, "delete_groups"):
            raise exceptions.TASK_GROUP_DELETE_NOT_PERMITTED

        await group.delete()

        return types.TaskGroup.from_ormar(group)


class CommentCreateMutation(graphene.Mutation):
    """
    Мутация graphql для создания комментария под задачей.
    """

    class Arguments:
        data = types.CommentCreate()

    Output = types.Comment

    @staticmethod
    @authorized_only
    async def mutate(_, __, user, data: types.CommentCreate):
        task: models.Task = await models.Task.objects.get_or_none(
            id=int(data.task_id)
        )

        if not task:
            raise exceptions.TASK_NOT_FOUND

        board: models.Board = task.group.board
        workspace: models.Workspace = board.workspace

        participant = await models.Participant.get_for_workspace(workspace, user)
        if not participant:
            raise exceptions.WORKSPACE_NOT_A_PARTICIPANT

        if not await board.check_permission(participant.role, "view_board"):
            raise exceptions.BOARD_VIEW_NOT_PERMITTED

        if not await board.check_permission(participant.role, "leave_comments"):
            raise exceptions.COMMENT_CREATE_NOT_PERMITTED

        comment = await models.Comment.objects.create(
            text=data.text,
            task=task,
            creator=participant,
        )

        return types.Comment.from_ormar(comment)


class CommentUpdateMutation(graphene.Mutation):
    """
    Мутация graphql для редактирования комментария
    """

    class Arguments:
        data = types.CommentUpdate()

    Output = types.Comment

    @staticmethod
    @authorized_only
    async def mutate(_, __, user, data: types.CommentUpdate):
        comment: models.Comment = await models.Comment.objects.get_or_none(
            id=int(data.id)
        )

        if not comment:
            raise exceptions.COMMENT_NOT_FOUND

        board: models.Board = comment.task.group.board
        workspace: models.Workspace = board.workspace

        participant = await models.Participant.get_for_workspace(workspace, user)
        if not participant:
            raise exceptions.WORKSPACE_NOT_A_PARTICIPANT

        if not await board.check_permission(participant.role, "view_board"):
            raise exceptions.BOARD_VIEW_NOT_PERMITTED

        if (
                comment.creator.id != participant.id
                and not await board.check_permission(participant.role, "update_foreign_comments")
        ):
            raise exceptions.COMMENT_UPDATE_NOT_PERMITTED

        await comment.update(
            text=data.text,
        )

        return types.Comment.from_ormar(comment)


class CommentDeleteMutation(graphene.Mutation):
    """
    Мутация graphql для удаления комментария с задачи.
    """

    class Arguments:
        comment_id = graphene.Argument(
            graphene.NonNull(graphene.ID)
        )

    Output = types.Comment

    @staticmethod
    @authorized_only
    async def mutate(_, __, user, comment_id: str):
        comment: models.Comment = await models.Comment.objects.get_or_none(
            id=int(comment_id)
        )

        if not comment:
            raise exceptions.COMMENT_NOT_FOUND

        board: models.Board = comment.task.group.board
        workspace: models.Workspace = board.workspace

        participant = await models.Participant.get_for_workspace(workspace, user)
        if not participant:
            raise exceptions.WORKSPACE_NOT_A_PARTICIPANT

        if not await board.check_permission(participant.role, "view_board"):
            raise exceptions.BOARD_VIEW_NOT_PERMITTED

        if (
            comment.creator.id != participant.id
            and not await board.check_permission(participant.role, "delete_foreign_comments")
        ):
            raise exceptions.COMMENT_DELETE_NOT_PERMITTED

        await comment.delete()

        return types.Comment.from_ormar(comment)


class CommentManageMutation(graphene.Mutation):
    """
    Мутация graphql для обновления статуса комментария
    """

    class Arguments:
        data = types.CommentManage()

    Output = types.Comment

    @staticmethod
    @authorized_only
    async def mutate(_, __, user, data: types.CommentManage):
        comment: models.Comment = await models.Comment.objects.get_or_none(
            id=int(data.id)
        )

        if not comment:
            raise exceptions.COMMENT_NOT_FOUND

        board: models.Board = comment.task.group.board
        workspace: models.Workspace = board.workspace

        participant = await models.Participant.get_for_workspace(workspace, user)
        if not participant:
            raise exceptions.WORKSPACE_NOT_A_PARTICIPANT

        if not await board.check_permission(participant.role, "view_board"):
            raise exceptions.BOARD_VIEW_NOT_PERMITTED

        if (
                comment.creator.id != participant.id
                and not await board.check_permission(participant.role, "manage_comments")
        ):
            raise exceptions.COMMENT_MANAGE_NOT_PERMITTED

        await comment.update(
            status=data.status
        )

        return types.Comment.from_ormar(comment)
