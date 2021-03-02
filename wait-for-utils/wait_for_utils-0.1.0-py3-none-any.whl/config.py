"""Config classes."""
import os
from dataclasses import dataclass


@dataclass
class _BaseConfig:
    """Base config."""

    timeout: int
    interval: int


@dataclass
class DBConfig(_BaseConfig):
    """Database config."""

    database: str = os.getenv("POSTGRES_DB", "postgres")
    user: str = os.getenv("POSTGRES_USER", "postgres")
    password: str = os.getenv("POSTGRES_PASSWORD", "")
    host: str = os.getenv("POSTGRES_HOST", "postgres")
    port: int = os.getenv("POSTGRES_PORT", "5432")

    timeout: int = os.getenv("POSTGRES_CHECK_TIMEOUT", 30)
    interval: int = os.getenv("POSTGRES_CHECK_INTERVAL", 1)
