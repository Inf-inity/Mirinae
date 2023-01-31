from enum import Enum, auto
from datetime import datetime
from typing import AsyncGenerator

from influxdb_client import Point
from influxdb_client.client.flux_table import FluxRecord
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from .environment import (
    DB_HOST,
    DB_PORT,
    MONGO_INITDB_ROOT_USERNAME as MIRU,
    MONGO_INITDB_ROOT_PASSWORD as MIRP,
    INFLUXDB_ADMIN_TOKEN as IAT,
    INFLUXDB_ORG as IO,
    INFLUX_PORT as IP,
    INFLUXDB_BUCKET as IB,
    INFLUX_URL as IU
)
from .logger import get_logger


logger = get_logger(__name__)

connect_string = f"mongodb://{MIRU}:{MIRP}@{DB_HOST}:{DB_PORT}/?authMechanism=DEFAULT"
client = AsyncIOMotorClient(connect_string)
db: AsyncIOMotorDatabase = client["bot_database"]


class Measurements(Enum):
    events = auto()
    startups = auto()


class Fields(Enum):
    on_auto_mod_action = auto()

    on_guild_available = auto()
    on_guild_join = auto()

    on_invite_create = auto()

    on_member_ban = auto()
    on_member_join = auto()
    on_member_remove = auto()

    on_message = auto()
    on_message_delete = auto()
    on_message_edit = auto()


class Cache:
    """cache class for the data-points"""
    point_cache: list[Point] = []

    def __int__(self):
        self.point_cache = []

    def reset(self):
        self.point_cache = []


cache = Cache()


class InfluxDB:
    @staticmethod
    def influx_decorator(func):
        async def inner(*args, **kwargs):
            async with InfluxDBClientAsync(url=f"http://{IU}:{IP}", token=IAT, org=IO) as influx_client:
                return await func(influx_client, *args, **kwargs)

        return inner

    @staticmethod
    def build_query(
            measurements: list[str],
            fields: list[str] | None,
            start: str = "-24h",
            stop: str = "now()",
            guild_id: int | None = None,
            bot: bool | None = None,
            interval: str = "10ms",
            fn: str = "last"
    ) -> str:
        query = f'from(bucket: "{IB}") |> range(start: {start}, stop: {stop})'
        query += ' |> filter(fn: (r) => ' + ' or '.join(
            f'r["_measurement"] == "{m}"' for m in measurements if m in Measurements.__dict__.get("_member_names_")
        ) + ')'

        filter_str = ' |> filter(fn: (r) => r["{}"] == "{}")'

        if fields:
            query += ' |> filter(fn: (r) => ' + ' or '.join(
                f'r["_field"] == "{f}"' for f in fields if f in Fields.__dict__.get("_member_names_")
            ) + ')'

        if guild_id:
            query += filter_str.format("guild_id", guild_id)
        if bot:
            query += filter_str.format("bot", bot)

        query += f' |> aggregateWindow(every: {interval}, fn: {fn}, createEmpty: false)'

        return query

    @staticmethod
    @influx_decorator
    async def insert_startup(i_client: InfluxDBClientAsync, /):
        data_point = Point("startups").field("startup", 1).time(datetime.utcnow())
        await i_client.write_api().write(bucket=IB, record=data_point)

    @staticmethod
    @influx_decorator
    async def insert_points(i_client: InfluxDBClientAsync, cached: list[Point]):
        await i_client.write_api().write(bucket=IB, record=cached)

    @staticmethod
    @influx_decorator
    async def execute_query(i_client: InfluxDBClientAsync, query: str) -> AsyncGenerator[FluxRecord, None]:
        return await i_client.query_api().query_stream(query=query)


class BasePost:
    collection: str
    datetime: datetime = datetime.utcnow()

    async def insert_in_collection(self):
        await db[self.collection].insert_one(self.serialize())

    def serialize(self):
        d = self.__dict__
        del d["collection"]
        return d

    @staticmethod
    async def find_in_collection(collection: str, search_filter: dict[str, ...], many: bool = False):
        if not many:
            return await db[collection].find_one(search_filter)
        return await db[collection].find(search_filter)

    @staticmethod
    async def update_data(collection: str, search_filter: dict[str, ...], updated: dict):
        return await db[collection].find_one_and_update(search_filter, update=updated)
