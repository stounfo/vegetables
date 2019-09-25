import asyncio

import sqlalchemy as sa
from aiopg.sa import create_engine

from orm_tables import (carts, carts_items, categories, products,
                        subcategories, users)
from utils import datetime_now


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

    async def get_user_id(self, user_code, client_type):
        user_id = False
        query = sa.select([users.c.user_id]).where(
                            (users.c.user_code == user_code) &
                            (users.c.client_type == client_type)                   
                        )

        async for row in self._conn.execute(query):
            user_id = row.user_id
        
        return user_id

    async def get_cart_id(self, user_id):
        cart_id = None
        query = sa.select([carts.c.cart_id]).where(carts.c.user_id == user_id)

        async for row in self._conn.execute(query):
            cart_id = row.cart_id
        
        return cart_id

    async def insert_into_users(self, user_code, client_type):
        result = await self._conn.execute(users.insert().values(
                user_code=user_code,
                client_type=client_type,
                name=None,
                phone=None,
                address=None,
                tms_create=datetime_now(),
        ))

        async for row in result:
            user_id = row[0]
        
        return user_id

    async def insert_into_carts(self, user_id):
        result = await self._conn.execute(carts.insert().values(
                user_id = user_id,
                tms_create=datetime_now(),
        ))

        async for row in result:
            cart_id = row[0]
        
        return cart_id