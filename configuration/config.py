from dataclasses import dataclass
from environs import Env


@dataclass
class DataBaseConfig:
    database_url: str


@dataclass
class Auth:
    secret_key: str
    algorithm: str
    token_expire: int


@dataclass
class App:
    host: str
    port: int


@dataclass
class Config:
    db: DataBaseConfig
    app: App
    auth: Auth
    debug: bool


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)
    
    return Config(
        db=DataBaseConfig(database_url=env('DATABASE_URL')),
        app=App(host=env('HOST'), port=int(env('PORT'))),
        auth=Auth(secret_key=env('SECRET_KEY'), algorithm=env('ALGORITHM'), token_expire=env('TOKEN')),
        debug=env.bool('DEBUG', default=False)
    )
