from os import getenv


def get_bool(key: str, default: bool) -> bool:
    """Get a boolean from an environment variable."""

    return getenv(key, str(default)).lower() in ("true", "t", "yes", "y", "1")


TOKEN: str | None = getenv("TOKEN")
LOG_LEVEL: str = getenv("LOG_LEVEL", "INFO")

# 0.0.0.0 / mongodb / localhost
DB_HOST: str = getenv("DB_HOST", "mongodbdb")
# 1998 / 27017
DB_PORT: int = int(getenv("DB_PORT", 27017))
MONGO_INITDB_ROOT_USERNAME: str = getenv("MONGO_INITDB_ROOT_USERNAME", "admin")
MONGO_INITDB_ROOT_PASSWORD: str = getenv("MONGO_INITDB_ROOT_PASSWORD", "admin")


# 0.0.0.0 / redis
REDIS_HOST: str = getenv("REDIS_HOST", "redis")
# 1999 / 6379
REDIS_PORT: int = int(getenv("REDIS_PORT", 6379))
REDIS_DB: int = int(getenv("REDIS_DB", 0))
CACHE_TTL: int = int(getenv("CACHE_TTL", 300))

INFLUXDB_ORG: str = getenv("DOCKER_INFLUXDB_INIT_ORG", "mirinae")
INFLUXDB_STARTUPS: str = getenv("DOCKER_INFLUXDB_INIT_BUCKET", "mirinae")
INFLUXDB_ADMIN_TOKEN: str = getenv("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN", "super_secret_token")
INFLUX_URL: str = getenv("INFLUX_URL", "0.0.0.0")
INFLUX_PORT: int = int(getenv("INFLUX_PORT", 8086))
