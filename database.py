import asyncio

import sqlalchemy as sa
from aiopg.sa import create_engine

from orm_tables import categories, kingdoms, products


class Database():
    def __init__(self, user, database, host, password):
        loop = asyncio.get_event_loop()
        self._conn = loop.run_until_complete(self._create_connection(user, 
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
            category = dict()
            for col in row:
                category[col] = row[col]
            list_of_kingdoms.append(category)
            
        return list_of_kingdoms

    async def select_categories(self, kingdom_id):
        list_of_categories = list()
        query = sa.select([categories]).where(categories.c.kingdom_id == kingdom_id)

        async for row in self._conn.execute(query):
            category = dict()
            for col in row:
                category[col] = row[col]
            list_of_categories.append(category)

        return list_of_categories

    async def select_products(self, category_id):
        list_of_products = list()
        query = sa.select([products]).where(products.c.category_id == category_id)

        async for row in self._conn.execute(query):
            product = dict()
            for col in row:
                product[col] = row[col]
            list_of_products.append(product)

        return list_of_products
