import asyncio

import sqlalchemy as sa
from aiopg.sa import create_engine

from orm_tables import categories, kingdoms, products


class Database():
    def __init__(self, user, database, host, password):
        self._loop = asyncio.get_event_loop()
        self._conn = self._loop.run_until_complete(self._create_connection(user, 
                                                                     database, 
                                                                     host, 
                                                                     password))

    async def _create_connection(self, user, database, host, password):
        engine = await create_engine(
            user=user,
            database=database,
            host=host,
            password=password
        )
        return await engine.acquire()

    async def select_kingdoms(self):
        list_of_kingdoms = list()

        query = sa.select([kingdoms])
        async for row in self._conn.execute(query):
            list_of_kingdoms.append({"kingdom_id": row.kingdom_id, "name": row.name})

        return list_of_kingdoms
