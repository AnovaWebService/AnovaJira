import fastapi
import uvicorn
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

import models
import settings
from graphql_service.core import schema
from models import Board, Workspace, database
from routers import users

app = fastapi.FastAPI(
    title="AnovaTask Backend",
    description="Бэкенд для нашего такс-менеджера.",
)
app.include_router(users.router)

graphql_app = GraphQLApp(schema=schema, on_get=make_graphiql_handler())
app.mount("/graphql/", graphql_app)


@app.on_event("startup")
async def on_startup():
    if not database.is_connected:
        await database.connect()

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


        import signals

        await models.User.objects.get_or_create(
            email="coolg1@mail.ru",
            _defaults={
                "password": "12345678",
                "first_name": "Kirill",
                "last_name": "Groshelev",
            }
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

