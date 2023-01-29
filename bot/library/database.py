from datetime import datetime

from influxdb_client import Point
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
    INFLUXDB_STARTUPS as IS,
    INFLUX_URL as IU
)

connect_string = f"mongodb://{MIRU}:{MIRP}@{DB_HOST}:{DB_PORT}/?authMechanism=DEFAULT"
client = AsyncIOMotorClient(connect_string)
db: AsyncIOMotorDatabase = client["bot_database"]


class Cache:
    """cache class for the data-points"""
    point_cache: list[Point] = []

    def __int__(self):
        self.point_cache = []

    def reset(self):
        self.point_cache = []


cache = Cache()


def influx_decorator(func):
    async def inner(*args, **kwargs):
        async with InfluxDBClientAsync(url=f"http://{IU}:{IP}", token=IAT, org=IO) as influx_client:
            return await func(influx_client, *args, **kwargs)

    return inner


class InfluxDB:
    @staticmethod
    @influx_decorator
    async def insert_startup(i_client: InfluxDBClientAsync, /):
        data_point = Point("startups").field("startup", 1).time(datetime.utcnow())
        await i_client.write_api().write(bucket=IS, record=data_point)

    @staticmethod
    @influx_decorator
    async def insert_points(i_client: InfluxDBClientAsync, cached: list[Point]):
        await i_client.write_api().write(bucket=IS, record=cached)


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
