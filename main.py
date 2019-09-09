from aiohttp import web
from database import Database
import json


async def get_kingdoms(request):
    list_of_kingdoms = await database.select_kingdoms()

    return web.Response(text=str(json.dumps(list_of_kingdoms, ensure_ascii=False)))



if __name__ == "__main__":
    database = Database(user="postgres",
                        database="vegetables",
                        host="localhost",
                        password="123")

    app = web.Application()
    app.add_routes([web.get("/get_kingdoms", get_kingdoms)])

    web.run_app(app, host="0.0.0.0", port=8081)
