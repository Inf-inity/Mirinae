from __future__ import annotations

from typing import Type

from discord.ext.commands.bot import Bot
from discord.ext.commands.cog import Cog as DiscordCog

from .logger import get_logger


logger = get_logger(__name__)


class Cog(DiscordCog):
    CONTRIBUTORS: list[tuple[str, int, str]]

    bot: Bot
    instance: None | Cog = None

    def __new__(cls, *args: ..., **kwargs: ...):
        # Make sure there exists only one instance of a cog.

        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)

            # set instance attribute of this and potential base classes
            c: Type[Cog]
            for c in cls.mro():
                if c is Cog:
                    break

                c.instance = c.instance or cls.instance

        return cls.instance

    async def load_all_cogs(self, bot: Bot):
        self.bot = bot
        for cog in list(Cog.__subclasses__()):
            logger.debug(f"{cog().__class__.__name__} loaded")
            await bot.add_cog(cog())
