from __future__ import annotations

from discord.ext.commands.bot import Bot
from discord.ext.commands.cog import Cog as DiscordCog

from .logger import get_logger


logger = get_logger(__name__)


class Cog(DiscordCog):
    CONTRIBUTORS: list[tuple[str, int, str]]

    @staticmethod
    async def load_all_cogs(bot: Bot):
        for cog in list(Cog.__subclasses__()):
            logger.debug(f"{cog().__cog_name__} loaded")
            await bot.add_cog(cog())
