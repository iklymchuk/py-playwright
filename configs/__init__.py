"""Configuration management module."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global settings from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )

    # Environment
    env: str = Field(default="dev", alias="ENV")
    base_url: str = Field(default="https://example.com", alias="BASE_URL")

    # Browser
    browser: str = Field(default="chromium", alias="BROWSER")
    headless: bool = Field(default=True, alias="HEADLESS")
    slow_mo: int = Field(default=0, alias="SLOW_MO")
    timeout: int = Field(default=30000, alias="TIMEOUT")

    # Test Execution
    parallel_workers: int = Field(default=4, alias="PARALLEL_WORKERS")
    retry_count: int = Field(default=2, alias="RETRY_COUNT")

    # Reporting
    report_type: str = Field(default="allure", alias="REPORT_TYPE")
    screenshot_on_failure: bool = Field(default=True, alias="SCREENSHOT_ON_FAILURE")
    video_on_failure: bool = Field(default=True, alias="VIDEO_ON_FAILURE")
    trace_on_failure: bool = Field(default=True, alias="TRACE_ON_FAILURE")

    # Test Data Service
    tds_base_url: str = Field(default="http://localhost:8080/api/v1", alias="TDS_BASE_URL")
    tds_api_key: str = Field(default="", alias="TDS_API_KEY")
    tds_timeout: int = Field(default=10, alias="TDS_TIMEOUT")

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_format: str = Field(default="json", alias="LOG_FORMAT")

    # Artifacts
    artifacts_path: str = Field(default="./artifacts", alias="ARTIFACTS_PATH")
    reports_path: str = Field(default="./reports", alias="REPORTS_PATH")

    # CI/CD
    ci: bool = Field(default=False, alias="CI")
    build_id: str = Field(default="local", alias="BUILD_ID")
    run_id: str = Field(default="local-run", alias="RUN_ID")


class ConfigLoader:
    """Load and manage YAML configuration files."""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize config loader."""
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                self._config = yaml.safe_load(f) or {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def get_env_config(self, env: str) -> Dict[str, Any]:
        """Get environment-specific configuration."""
        return self._config.get(env, {})

    def get_browser_config(self, browser: str) -> Dict[str, Any]:
        """Get browser-specific configuration."""
        browsers = self._config.get("browsers", {})
        return browsers.get(browser, {})

    def get_device_config(self, device: str) -> Dict[str, Any]:
        """Get device-specific configuration."""
        devices = self._config.get("devices", {})
        return devices.get(device, {})

    def get_execution_config(self) -> Dict[str, Any]:
        """Get execution configuration."""
        return self._config.get("execution", {})


# Global instances
settings = Settings()
config_loader = ConfigLoader()


def get_settings() -> Settings:
    """Get global settings instance."""
    return settings


def get_config_loader() -> ConfigLoader:
    """Get global config loader instance."""
    return config_loader


def get_base_url(env: Optional[str] = None) -> str:
    """Get base URL for environment."""
    env = env or settings.env
    env_config = config_loader.get_env_config(env)
    return env_config.get("base_url", settings.base_url)


def get_api_url(env: Optional[str] = None) -> str:
    """Get API URL for environment."""
    env = env or settings.env
    env_config = config_loader.get_env_config(env)
    return env_config.get("api_url", "")