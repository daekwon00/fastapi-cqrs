from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "admin"
    DB_PASSWORD: str = ""
    DB_NAME: str = "intranet"
    DB_SCHEMA: str = "internal"

    # JWT
    JWT_SECRET: str = ""
    JWT_ACCESS_EXPIRATION: int = 3600000  # 1시간 (ms)
    JWT_REFRESH_EXPIRATION: int = 604800000  # 7일 (ms)

    # File Upload
    FILE_UPLOAD_DIR: str = "./uploads"

    # Server
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8082

    # AI
    AI_DEFAULT_PROVIDER: str = "anthropic"
    AI_ANTHROPIC_API_KEY: str = ""
    AI_ANTHROPIC_MODEL: str = "claude-sonnet-4-20250514"
    AI_OPENAI_API_KEY: str = ""
    AI_OPENAI_MODEL: str = "gpt-4o"
    AI_GEMINI_API_KEY: str = ""
    AI_GEMINI_MODEL: str = "gemini-2.0-flash"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
