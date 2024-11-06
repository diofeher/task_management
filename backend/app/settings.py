from pydantic_settings import BaseSettings


class Settings(BaseSettings):  # type: ignore
    # TODO: Remove this hardcoded default from here
    database_url: str = (
        # "postgresql+psycopg2://myuser:mypassword@db:5432/mydatabase"
        "postgresql+psycopg2://myuser:mypassword@localhost:5432/mydatabase"
    )


settings = Settings()
