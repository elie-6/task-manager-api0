from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str

    # Database name for your Task Manager project
    MONGODB_DATABASE: str = "task_manager_db"

    # Collection name for tasks
    MONGODB_COLLECTION: str = "tasks"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
