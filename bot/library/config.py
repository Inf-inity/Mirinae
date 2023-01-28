import yaml
from pathlib import Path
from subprocess import getoutput

from .contributor import Contributor


class Config:
    NAME: str
    VERSION: str

    # repository information
    REPO_OWNER: str
    REPO_NAME: str
    REPO_LINK: str
    REPO_ICON: str | None

    # pydrocsid information
    DOCUMENTATION_URL: str | None
    DISCORD_INVITE: str | None

    # developers
    CONTRIBUTORS: list[tuple[str, int, str]]


def load_repo(config: dict[str, ...]) -> None:
    """Load repository configuration."""

    Config.REPO_OWNER = config["repo"]["owner"]
    Config.REPO_NAME = config["repo"]["name"]
    Config.REPO_LINK = f"https://github.com/{Config.REPO_OWNER}/{Config.REPO_NAME}"
    Config.REPO_ICON = config["repo"]["icon"] or None

    Config.DOCUMENTATION_URL = config["repo"]["documentation_url"] or None
    Config.DISCORD_INVITE = config["repo"]["discord_invite"] or None

    Config.VERSION = getoutput("git describe --tags --always")


def load_config_file(path: Path) -> None:

    with path.open() as file:
        config = yaml.safe_load(file)

    Config.NAME = config["name"]
    Config.AUTHOR = config["author"]
    Config.CONTRIBUTORS = Contributor.ALL

    load_repo(config)
