import asyncio
import random
from typing import Union

import sqlalchemy as sa
from aiopg.sa import create_engine

from orm_tables import (carts, carts_items, categories, orders, products,
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

    async def select_categories(self) -> list:
        list_of_categories = list()
        query = sa.select([categories])

        async for row in self._conn.execute(query):
            subcategory = dict()
            for col in row:
                subcategory[col] = row[col]
            list_of_categories.append(subcategory)

        return list_of_categories

    async def select_subcategories(self, category_id: int) -> list:
        list_of_subcategories = list()
        query = sa.select([subcategories]).where(
            subcategories.c.category_id == category_id)

        async for row in self._conn.execute(query):
            subcategory = dict()
            for col in row:
                subcategory[col] = row[col]
            list_of_subcategories.append(subcategory)

        return list_of_subcategories

    async def select_products(self, subcategory_id: int) -> list:
        list_of_products = list()
        query = sa.select([products]).where(
            products.c.subcategory_id == subcategory_id)

        async for row in self._conn.execute(query):
            product = dict()
            for col in row:
                product[col] = row[col]
            list_of_products.append(product)

        return list_of_products

    async def user_exists(self, user_code: str, client_type: str) -> Union[int, bool]:
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
        query = sa.select([carts.c.cart_id]).where((carts.c.user_id == user_id) &
                                                   (carts.c.status == "cart"))

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
            user_id=user_id,
            status="cart",
            tms_create=datetime_now(),
        ))

        async for row in result:
            cart_id = row[0]

        return cart_id

    async def get_cart_item_id(self, cart_id, product_id):
        cart_item_id = False
        query = sa.select([carts_items.c.cart_item_id]).where(
            (carts_items.c.cart_id == cart_id) &
            (carts_items.c.product_id == product_id)
        )

        async for row in self._conn.execute(query):
            cart_item_id = row.cart_item_id

        return cart_item_id

    async def update_cart_item(self, cart_item_id, quantity):
        await self._conn.execute(carts_items.update().values(
            quantity=quantity).where(
            carts_items.c.cart_item_id == cart_item_id
        ))

    async def insert_into_carts_items(self, cart_id, product_id, quantity):
        await self._conn.execute(carts_items.insert().values(quantity=quantity,
                                                             product_id=product_id,
                                                             cart_id=cart_id))

    async def get_cart_items(self, cart_id):
        # TODO rename to select
        cart_items = list()
        join = sa.join(carts_items, products,
                       carts_items.c.product_id == products.c.product_id)
        query = sa.select([carts_items, products.c.name]).select_from(
            join).where(carts_items.c.cart_id == cart_id)

        async for row in self._conn.execute(query):
            item = dict()
            for col in row:
                item[col] = row[col]
            cart_items.append(item)

        return cart_items

    async def delete_item_from_cart(self, cart_id, product_id):
        await self._conn.execute(carts_items.delete().where((carts_items.c.cart_id == cart_id) &
                                                            (carts_items.c.product_id == product_id)))

    async def select_user(self, user_code, client_type):
        # TODO select all users col
        user_info = dict()
        query = sa.select([users.c.name, users.c.phone, users.c.address]).where((users.c.user_code == user_code) &
                                                                                (users.c.client_type == client_type))

        async for row in self._conn.execute(query):
            for col in row:
                user_info[col] = row[col]

        return user_info

    async def update_user_info(self, user_code: str, client_type: str,
                               name: str, phone: str, address: str):
        query = users.update().values(name=name, phone=phone, address=address).where(
            (users.c.user_code == user_code) &
            (users.c.client_type == client_type))

        await self._conn.execute(query)

    async def insert_into_order(self, user_id, order_time, phone, address, order_products, cart_id):
        result = await self._conn.execute(orders.insert().values(
            tms_create=datetime_now(),
            user_id=user_id,
            order_time=order_time,
            phone=phone,
            address=address,
            order_products=order_products,
            cart_id=cart_id,
            code=str(random.randrange(100000, 999999)),
            status="active"))

    async def change_cart_status(self, cart_id: int, status: str):
        query = carts.update().values(status=status).where(carts.c.cart_id == cart_id)
        await self._conn.execute(query)

    async def select_user_orders(self, user_id, status):
        user_orders = list()
        query = sa.select([orders]).where((orders.c.user_id == user_id) &
                                          (orders.c.status == status))

        async for row in self._conn.execute(query):
            order = dict()
            for col in row:
                order[col] = row[col]
            user_orders.append(order)

        return user_orders


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    database = Database(user="vegetables",
                        database="vegetables",
                        host="localhost",
                        password="vegetables")

    print(loop.run_until_complete(
        database.change_cart_status(cart_id=1, status="cart")))
