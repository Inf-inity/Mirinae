import sys
from pathlib import Path

from library.config import Config, load_config_file

from discord import Intents
from discord.ext.commands import Bot

from cogs import *

from library.database import InfluxDB
from library.cog import Cog
from library.environment import TOKEN
from library.logger import ColorFormatter, get_logger


logger = get_logger(__name__)

mirinae = Bot(
    command_prefix=",",
    case_insensitive=True,
    intents=Intents.all(),
    # help_command=None,
    strip_after_prefix=True,
    owner_ids=[846009958062358548]
)


@mirinae.event
async def on_ready():
    logger.info("Loading Cogs")
    await Cog.load_all_cogs(mirinae)
    logger.debug("Setting startup-time")
    await InfluxDB.insert_startup()


def run():
    if not TOKEN:
        logger.critical("TOKEN not found!")
        sys.exit(1)

    logger.debug("Loading Config")
    load_config_file(Path("config.yml"))

    logger.info(f"Starting {Config.NAME} v{Config.VERSION} ({Config.REPO_LINK})")

    mirinae.run(token=TOKEN, log_formatter=ColorFormatter())
