from .db import DatabaseConfig

settings = DatabaseConfig()
tortoise_settings = settings.tortoise_config