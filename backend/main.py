import fastapi
import uvicorn

import settings
from models import database

app = fastapi.FastAPI(
    title="AnovaTask Backend",
    description="Бэкенд для нашего такс-менеджера.",
)


@app.on_event("startup")
async def on_startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.HOST,
        port=settings.PORT,
    )

