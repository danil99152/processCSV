import pathlib

from pydantic import conint, constr


class Settings:
    DEBUG: bool = True

    APP_HOST: constr(min_length=1, max_length=15) = str('127.0.0.1' if DEBUG else '0.0.0.0')
    APP_PORT: conint(ge=0) = 5000
    APP_PATH: constr(min_length=1, max_length=255) = str(pathlib.Path(__file__).parent.resolve())


settings = Settings()
