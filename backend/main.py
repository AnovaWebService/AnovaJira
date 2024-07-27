import fastapi
import uvicorn
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

import models
import settings
from graphql_service.core import schema
from models import database, Workspace, Board

app = fastapi.FastAPI(
    title="AnovaTask Backend",
    description="Бэкенд для нашего такс-менеджера.",
)

graphql_app = GraphQLApp(schema=schema, on_get=make_graphiql_handler())
app.mount("/graphql/", graphql_app)


@app.on_event("startup")
async def on_startup():
    if not database.is_connected:
        await database.connect()
        import signals

        for permission in Board.permissions:
            await models.Permission.objects.get_or_create(
                code=permission,
                instance_class="Board"
            )

        for permission in Workspace.permissions:
            await models.Permission.objects.get_or_create(
                code=permission,
                instance_class="Workspace"
            )


@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.HOST,
        port=settings.PORT,
    )

