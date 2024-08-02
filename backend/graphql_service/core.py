import graphene

from . import mutations, subscriptions
from .query import Query


class Subscription(
    subscriptions.WorkspaceSubscription,
    subscriptions.TaskSubscription,
    subscriptions.BoardSubscription,
    subscriptions.RoleSubscription,
    subscriptions.CommentsSubscription,
    subscriptions.PermissionSubscription,
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
    create_group = mutations.TaskGroupCreateMutation.Field()
    update_group = mutations.TaskGroupUpdateMutation.Field()
    delete_group = mutations.TaskGroupDeleteMutation.Field()
    create_task = mutations.TaskCreateMutation.Field()
    update_task = mutations.TaskUpdateMutation.Field()
    # delete_task = mutations.TaskDeleteMutation.Field()
    create_comment = mutations.CommentCreateMutation.Field()
    update_comment = mutations.CommentUpdateMutation.Field()
    manage_comment = mutations.CommentManageMutation.Field()
    delete_comment = mutations.CommentDeleteMutation.Field()


schema = graphene.Schema(
    subscription=Subscription,
    mutation=Mutation,
    query=Query
)
