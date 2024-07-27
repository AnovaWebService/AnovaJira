import graphene

import models

from . import mutations, subscriptions, types


class Subscription(
    subscriptions.WorkspaceSubscription,
    subscriptions.TaskSubscription,
    subscriptions.BoardSubscription,
    subscriptions.RoleSubscription,
    subscriptions.CommentsSubscription,
    graphene.ObjectType,
):
    """
    Подписки для обновления данных в реальном времени
    """


class Mutation(graphene.ObjectType):
    """
    Все доступные мутации проекта
    """

    create_workspace = mutations.WorkspaceCreateMutation.Field()
    update_workspace = mutations.WorkspaceUpdateMutation.Field()
    create_board = mutations.BoardCreateMutation.Field()
    update_board = mutations.BoardUpdateMutation.Field()
    delete_board = mutations.BoardDeleteMutation.Field()


class Query(graphene.ObjectType):
    """
    Все доступные запросы
    """

    workspaces = graphene.List(types.Workspace)
    roles = graphene.List(types.Role, workspace_id=graphene.Int())
    boards = graphene.List(types.Board, workspace_id=graphene.Int())
    comments = graphene.List(types.Board, task_id=graphene.Int())
    tasks = graphene.List(types.Board, board_id=graphene.Int())

    @staticmethod
    async def resolve_workspaces(root, info):
        return await models.Workspace.objects.all()

    @staticmethod
    async def resolve_roles(root, info, workspace_id: int):
        return await models.Role.objects.filter(workspace__id=workspace_id).all()

    @staticmethod
    async def resolve_boards(root, info, workspace_id: int):
        return await models.Board.objects.filter(workspace__id=workspace_id).all()

    @staticmethod
    async def resolve_comments(root, info, task_id: int):
        return await models.Comment.objects.filter(task__id=task_id).all()

    @staticmethod
    async def resolve_tasks(root, info, board_id: int):
        return await models.Task.objects.filter(
            group__board__id=board_id,
        )


schema = graphene.Schema(
    subscription=Subscription,
    mutation=Mutation,
    query=Query
)

