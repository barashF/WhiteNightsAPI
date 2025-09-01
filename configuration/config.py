from dataclasses import dataclass

from environs import Env


@dataclass
class DataBaseConfig:
    database_user: str
    database_password: str
    database_host: str
    database_port: int
    database_name: str


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
class Broker:
    user: str
    password: str
    host: str


@dataclass
class Config:
    db: DataBaseConfig
    app: App
    auth: Auth
    broker: Broker
    debug: bool


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        db=DataBaseConfig(
            database_user=env("DB_USER"),
            database_password=env("DB_PASSWORD"),
            database_host=env("DB_HOST"),
            database_port=env("DB_PORT"),
            database_name=env("DB_NAME"),
        ),
        app=App(host=env("HOST"), port=int(env("PORT"))),
        auth=Auth(
            secret_key=env("SECRET_KEY"),
            algorithm=env("ALGORITHM"),
            token_expire=env("TOKEN"),
        ),
        broker=Broker(
            user=env("RABBIT_USER"),
            password=env("RABBIT_PASSWORD"),
            host=env("RABBIT_HOST"),
        ),
        debug=env.bool("DEBUG", default=False),
    )
