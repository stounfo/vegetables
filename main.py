from aiohttp import web
from database import Database
import json

routes = web.RouteTableDef()


@routes.get('/get_kingdoms')
async def get_kingdoms(request):
    kingdoms = await database.select_kingdoms()
    return web.json_response(kingdoms)


@routes.post('/get_categories')
async def get_categories(request):
    kingdom_id = await request.json()
    categories = await database.select_categories(kingdom_id["kingdom_id"])
    return web.json_response(categories)


@routes.post('/get_products')
async def get_products(request):
    category_id = await request.json()    
    products = await database.select_products(category_id["category_id"])
    return web.json_response(products)



if __name__ == "__main__":
    database = Database(user="vegetables",
                        database="vegetables",
                        host="vegetables-pg",
                        password="vegetables")
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host="0.0.0.0", port=8080)
