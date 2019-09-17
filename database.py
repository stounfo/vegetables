import asyncio

import sqlalchemy as sa
from aiopg.sa import create_engine

from orm_tables import subcategories, categories, products


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

    async def select_categories(self):
        list_of_categories = list()
        query = sa.select([categories])

        async for row in self._conn.execute(query):
            subcategory = dict()
            for col in row:
                subcategory[col] = row[col]
            list_of_categories.append(subcategory)
            
        return list_of_categories

    async def select_subcategories(self, category_id):
        list_of_subcategories = list()
        query = sa.select([subcategories]).where(subcategories.c.category_id == category_id)

        async for row in self._conn.execute(query):
            subcategory = dict()
            for col in row:
                subcategory[col] = row[col]
            list_of_subcategories.append(subcategory)

        return list_of_subcategories

    async def select_products(self, subcategory_id):
        list_of_products = list()
        query = sa.select([products]).where(products.c.subcategory_id == subcategory_id)

        async for row in self._conn.execute(query):
            product = dict()
            for col in row:
                product[col] = row[col]
            list_of_products.append(product)

        return list_of_products
