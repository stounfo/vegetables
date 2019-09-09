from aiohttp import web
<<<<<<< HEAD
import json

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
=======
from database import Database


async def get_kingdoms(request):
    list_of_kingdoms = await database.select_kingdoms()
>>>>>>> 75d8ac1

    return web.Response(text=str(json.dumps(list_of_kingdoms, ensure_ascii=False)))



if __name__ == "__main__":
    database = Database(user="postgres",
                        database="vegetables",
                        host="localhost",
                        password="123")

    app = web.Application()
<<<<<<< HEAD
    conn = asyncio.get_event_loop().run_until_complete(_create_connection())

    app.add_routes([web.get('/get_kingdoms', get_kingdoms)])
=======
    app.add_routes([web.get("/get_kingdoms", get_kingdoms)])
>>>>>>> 75d8ac1

    web.run_app(app, host="0.0.0.0", port=8081)
