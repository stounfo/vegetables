from aiohttp import web
from database import Database
import json

routes = web.RouteTableDef()


@routes.get('/get_categories')
async def get_categories(request):
    categories = await database.select_categories()
    return web.json_response(categories)


@routes.post('/get_subcategories')
async def get_subcategories(request):
    category_id = await request.json()
    subcategories = await database.select_subcategories(category_id["category_id"])
    return web.json_response(subcategories)


@routes.post('/get_products')
async def get_products(request):
    subcategory_id = await request.json()    
    products = await database.select_products(subcategory_id["subcategory_id"])
    return web.json_response(products)



if __name__ == "__main__":
    database = Database(user="vegetables",
                        database="vegetables",
                        host="vegetables-pg",
                        password="vegetables")
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host="0.0.0.0", port=8080)
