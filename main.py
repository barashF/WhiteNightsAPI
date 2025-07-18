import uvicorn

from application import app
from configuration.config import load_config


# config = load_config("/app/.env_test")
config = load_config("/home/vitaly/Рабочий стол/WhiteNights/.env")

if __name__ == "__main__":
    uvicorn.run(app.create_app(), host=config.app.host, port=config.app.port)
