from fastapi import FastAPI

from application.middlewares.exception_middleware import ExceptionMiddleware
from application.routers import group, place, user


def _init_routers(app: FastAPI):
    app.include_router(user.router)
    app.include_router(place.router)
    app.include_router(group.router)


def create_app():
    app = FastAPI(title="White Nights", docs_url="/api/swagger")
    _init_routers(app)
    app.add_middleware(ExceptionMiddleware)
    return app
