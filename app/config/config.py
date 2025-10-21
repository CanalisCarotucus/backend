from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings."""

    # Environment configuration
    env: str = Field(default="dev", description="Environment (dev/prod)")
    database_url_async: Optional[str] = Field(
        default=None, description="Async database URL"
    )

    # Server configuration
    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=8081, description="Server port")
    debug: bool = Field(default=True, description="Debug mode")

    # API documentation
    docs_url: Optional[str] = Field(default="/docs", description="Swagger docs URL")
    redoc_url: Optional[str] = Field(default="/redoc", description="ReDoc URL")

    # CORS origins
    origins: List[str] = Field(
        default_factory=lambda: ["*"], description="CORS allowed origins"
    )

    # Base directory
    base_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent,
        description="Base directory",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._configure_environment_specific_settings()

    def _configure_environment_specific_settings(self):
        """Configure settings based on environment."""
        if self.env == "prod":
            # Production settings
            self.host = "0.0.0.0"
            self.port = 8080
            self.debug = False
            self.docs_url = None
            self.redoc_url = None
            self.origins = [
                "https://example.com",
                "http://example.com",
                "https://api.example.com",
                "http://api.example.com",
            ]
        else:
            # Development settings
            self.host = "127.0.0.1"
            self.port = 8081
            self.debug = True
            self.docs_url = "/docs"
            self.redoc_url = "/redoc"
            self.origins = ["*"]


# Create settings instance
settings = Settings()
