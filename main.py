from application import app
from configuration.config import load_config
import uvicorn
import asyncio


config = load_config('/home/vitaly/Рабочий стол/WhiteNights/.env_test')


if __name__ == '__main__':
    uvicorn.run(app.create_app(), host=config.app.host, port=config.app.port)