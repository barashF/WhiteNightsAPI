from fastapi import FastAPI

from application.middlewares.exception_middleware import ExceptionMiddleware
from application.routers import user

def _init_routers(app: FastAPI):
    app.include_router(user.router)


def create_app():
    app = FastAPI(
        title='White Nights',
        docs_url='/api/swagger'
    )
    _init_routers(app)
    app.add_middleware(ExceptionMiddleware)
    return app
