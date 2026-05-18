from fastapi import FastAPI
from src.core.exceptions import handlers as exception_handlers
from src.api.rest.routes import user_routes
from src.api.rest.routes import auth_routes
from contextlib import asynccontextmanager
from src.data.clients.postgress_client import init_async_engine, dispose_async_engine
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_async_engine()
    yield
    await dispose_async_engine()

def get_app():
    app = FastAPI(lifespan=lifespan)
    # register all app-specific exception handlers centrally

    app.include_router(user_routes.router)
    app.include_router(auth_routes.router)
    exception_handlers.register_exception_handlers(app)
    return app
