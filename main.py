from aiohttp import web
from database import Database
import json


async def get_kingdoms(request):
    list_of_kingdoms = await database.select_kingdoms()
    return web.json_response(list_of_kingdoms)


async def get_categories(request):
    list_of_categories = await database.select_categories(3)
    return web.json_response(list_of_categories)



if __name__ == "__main__":
    database = Database(user="postgres",
                        database="vegetables",
                        host="localhost",
                        password="123")

    app = web.Application()
    app.add_routes([web.get("/get_kingdoms", get_kingdoms),
                    web.post("/get_categories", get_categories)])

    web.run_app(app, host="0.0.0.0", port=8082)
