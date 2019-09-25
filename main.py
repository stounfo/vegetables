from aiohttp import web
import aiohttp_cors
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


@routes.post('/get_cart_id')
async def get_cart_id(request):
    request_data = await request.json()
    user_code = request_data["user_code"]
    client_type = request_data["client_type"]

    user_id = await database.get_user_id(user_code, client_type)

    if user_id:
        cart_id = await database.get_cart_id(user_id)
        return web.json_response({"cart_id": cart_id})
    else:
        user_id = await database.insert_into_users(user_code, client_type)
        cart_id = await database.insert_into_carts(user_id)
        return web.json_response({"cart_id": cart_id})



if __name__ == "__main__":
    # Add conn to db
    database = Database(user="vegetables",
                        database="vegetables",
                        host="localhost",
                        password="vegetables")
    app = web.Application()
    app.add_routes(routes)

    # Add CORS for all routes
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(expose_headers="*", allow_headers="*")
    })
    for route in list(app.router.routes()):
        cors.add(route)

    # Run server
    web.run_app(app, host="0.0.0.0", port=8080)
