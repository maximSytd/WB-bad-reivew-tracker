import pathlib

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = pathlib.Path(__file__).parents[2]
ENV_FILE_PATH = ROOT_DIR.joinpath(".env")

class DatabaseConfig(BaseSettings):
    """Database connection config."""
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="postgres")
    postgres_db: str = Field(default="postgres")
    postgres_dsn: str = Field(default="")

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
    )

    @computed_field(return_type=str)
    def postgres_connection_string(self):
        """Return string of postgres dsn."""
        return self.postgres_dsn or f'postgres://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'

    @computed_field(return_type=dict)
    def tortoise_config(self):
        return {
            'connections': {
                'default': self.postgres_connection_string,
            },
            'apps': {
                'wb-bad-review-tracker': {
                    'models': [
                        'aerich.models',
                        'core.models',
                    ],
                },
            },
        }
