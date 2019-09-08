import asyncio
from aiopg.sa import create_engine
import sqlalchemy as sa
from orm_tables import kingdoms, products, categories
from aiohttp import web

async def _create_connection():
    engine = await create_engine(
        user="postgres",
        database="vegetables",
        host="localhost",
        password="123"
    )

    return await engine.acquire()


async def get_kingdoms(request):
    list_of_kingdoms = list()

    query = sa.select([kingdoms])
    async for row in conn.execute(query):
        list_of_kingdoms.append({"kingdom_id": row.kingdom_id, "name": row.name})

    return web.Response(text=str(list_of_kingdoms))
    


if __name__ == "__main__":
    app = web.Application()
    conn = asyncio.get_event_loop().run_until_complete(_create_connection())
    app.add_routes([web.get('/get_kingdoms', get_kingdoms)])

    web.run_app(app, host='0.0.0.0', port=8081)
