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

    @debug_command.group(name="cache", aliases=["c"])
    async def cache(self, ctx: Context):
        pass

    @cache.command(name="print", aliases=["p"])
    async def print_cache(self, _: Context):
        logger.debug(cache.point_cache)

    @cache.command("insert", aliases=["i"])
    async def insert_cache(self, _: Context):
        logger.info("Inserting cache in Influx")
        await InfluxDB.insert_points(cached=cache.point_cache)
        cache.reset()

    @debug_command.group(name="influx", aliases=["i"])
    async def influx_command(self, _: Context):
        pass

    @influx_command.group(name="query", aliases=["q"])
    async def query_test(self, _: Context):
        pass

    @query_test.command(name="execute", aliases=["e"])
    async def execute_query(self, _: Context, *, query: str):
        logger.debug(f"executing query: '{query}'")
        res = await InfluxDB.execute_query(query)
