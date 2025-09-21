"""Configuration management for the AI Financial Multi-Agent System."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file from project root
project_root = Path(__file__).parent.parent.parent.parent
env_file = project_root / ".env"
if env_file.exists():
    load_dotenv(env_file)
    print(f"✅ Loaded .env file from: {env_file}")
else:
    print(f"⚠️  .env file not found at: {env_file}")


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    # PostgreSQL settings
    postgres_host: str = Field(default="localhost", env="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, env="POSTGRES_PORT")
    postgres_user: str = Field(default="ai_financial", env="POSTGRES_USER")
    postgres_password: str = Field(default="", env="POSTGRES_PASSWORD")
    postgres_db: str = Field(default="ai_financial", env="POSTGRES_DB")
    
    # MongoDB settings
    mongodb_url: str = Field(default="mongodb://localhost:27017", env="MONGODB_URL")
    mongodb_db: str = Field(default="ai_financial", env="MONGODB_DB")
    
    # Redis settings
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    redis_db: int = Field(default=0, env="REDIS_DB")
    
    @property
    def postgres_url(self) -> str:
        """Get PostgreSQL connection URL."""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


class LLMSettings(BaseSettings):
    """LLM and AI model configuration."""
    
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4-turbo-preview", env="OPENAI_MODEL")
    openai_temperature: float = Field(default=0.1, env="OPENAI_TEMPERATURE")
    openai_max_tokens: int = Field(default=4000, env="OPENAI_MAX_TOKENS")
    
    # Langfuse settings for monitoring
    langfuse_secret_key: str = Field(default="", env="LANGFUSE_SECRET_KEY")
    langfuse_public_key: str = Field(default="", env="LANGFUSE_PUBLIC_KEY")
    langfuse_host: str = Field(default="https://cloud.langfuse.com", env="LANGFUSE_HOST")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
    
    @property
    def has_openai_key(self) -> bool:
        """Check if OpenAI API key is configured."""
        return bool(self.openai_api_key and self.openai_api_key.startswith("sk-"))


class SecuritySettings(BaseSettings):
    """Security and authentication configuration."""
    
    secret_key: str = Field(default="", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Encryption settings
    encryption_key: str = Field(default="", env="ENCRYPTION_KEY")
    
    @validator("secret_key")
    def validate_secret_key(cls, v: str) -> str:
        if not v:
            # Generate a default key for development
            import secrets
            import string
            default_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
            print(f"WARNING: Using auto-generated SECRET_KEY for development. Set SECRET_KEY environment variable for production.")
            return default_key
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v


class MonitoringSettings(BaseSettings):
    """Monitoring and observability configuration."""
    
    # OpenTelemetry settings
    otel_service_name: str = Field(default="ai-financial-system", env="OTEL_SERVICE_NAME")
    otel_exporter_otlp_endpoint: str = Field(default="", env="OTEL_EXPORTER_OTLP_ENDPOINT")
    otel_exporter_otlp_headers: str = Field(default="", env="OTEL_EXPORTER_OTLP_HEADERS")
    
    # Logging settings
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")  # json or text
    
    # Metrics settings
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=8000, env="METRICS_PORT")


class MCPSettings(BaseSettings):
    """Model Context Protocol configuration."""
    
    mcp_server_host: str = Field(default="localhost", env="MCP_SERVER_HOST")
    mcp_server_port: int = Field(default=8001, env="MCP_SERVER_PORT")
    mcp_tool_timeout: int = Field(default=30, env="MCP_TOOL_TIMEOUT")
    
    # Tool configuration
    enabled_tools: List[str] = Field(default_factory=lambda: [
        "memory_tools",
        "calculation_tools",
        "integration_tools",
        "communication_tools"
    ])


class ExternalIntegrationSettings(BaseSettings):
    """External system integration configuration."""
    
    # QuickBooks integration
    quickbooks_client_id: str = Field(default="", env="QUICKBOOKS_CLIENT_ID")
    quickbooks_client_secret: str = Field(default="", env="QUICKBOOKS_CLIENT_SECRET")
    quickbooks_sandbox: bool = Field(default=True, env="QUICKBOOKS_SANDBOX")
    
    # Banking API settings
    plaid_client_id: str = Field(default="", env="PLAID_CLIENT_ID")
    plaid_secret: str = Field(default="", env="PLAID_SECRET")
    plaid_environment: str = Field(default="sandbox", env="PLAID_ENVIRONMENT")
    
    # OCR settings
    tesseract_path: str = Field(default="/usr/bin/tesseract", env="TESSERACT_PATH")
    ocr_confidence_threshold: float = Field(default=0.8, env="OCR_CONFIDENCE_THRESHOLD")


class WorkflowSettings(BaseSettings):
    """Workflow and processing configuration."""
    
    # Advisory workflow settings
    cash_flow_forecast_weeks: int = Field(default=13, env="CASH_FLOW_FORECAST_WEEKS")
    pl_forecast_months: int = Field(default=12, env="PL_FORECAST_MONTHS")
    
    # Transactional workflow settings
    auto_approval_threshold: float = Field(default=1000.0, env="AUTO_APPROVAL_THRESHOLD")
    two_man_rule_threshold: float = Field(default=5000.0, env="TWO_MAN_RULE_THRESHOLD")
    
    # Processing settings
    batch_size: int = Field(default=100, env="BATCH_SIZE")
    max_concurrent_agents: int = Field(default=10, env="MAX_CONCURRENT_AGENTS")


class Settings(BaseSettings):
    """Main application settings."""
    
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # API settings
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_prefix: str = Field(default="/api/v1", env="API_PREFIX")
    
    # Component settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    monitoring: MonitoringSettings = Field(default_factory=MonitoringSettings)
    mcp: MCPSettings = Field(default_factory=MCPSettings)
    external: ExternalIntegrationSettings = Field(default_factory=ExternalIntegrationSettings)
    workflow: WorkflowSettings = Field(default_factory=WorkflowSettings)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env
    
    @validator("environment")
    def validate_environment(cls, v: str) -> str:
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v
    
    def get_database_url(self, db_type: str = "postgres") -> str:
        """Get database connection URL by type."""
        if db_type == "postgres":
            return self.database.postgres_url
        elif db_type == "mongodb":
            return self.database.mongodb_url
        elif db_type == "redis":
            return self.database.redis_url
        else:
            raise ValueError(f"Unknown database type: {db_type}")
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings instance."""
    return settings