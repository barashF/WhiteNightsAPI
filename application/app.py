from fastapi import FastAPI


def _init_routers(app: FastAPI):
    pass


def create_app():
    app = FastAPI(
        title='White Nights',
        docs_url='/api/swagger'
    )
    _init_routers(app)

    return app
