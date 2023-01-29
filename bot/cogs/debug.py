from discord.ext import commands
from discord.ext.commands import Context, is_owner

from library.cog import Cog
from library.contributor import Contributor
from library.database import InfluxDB, cache
from library.logger import get_logger


logger = get_logger(__name__)


class DebugCog(Cog):
    CONTRIBUTORS = [Contributor.Infinity]

    @commands.group(name="debug")
    @is_owner()
    async def debug_command(self, ctx: Context):
        pass

    @debug_command.group(name="cache")
    async def cache(self, ctx: Context):
        pass

    @cache.command(name="print")
    async def print_cache(self, _: Context):
        logger.debug(cache.point_cache)

    @cache.command("insert")
    async def insert_cache(self, _: Context):
        logger.info("Inserting cache in Influx")
        await InfluxDB.insert_points(cached=cache.point_cache)
        cache.reset()
