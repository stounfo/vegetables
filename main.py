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
    user_code = str(request_data["user_code"])
    client_type = request_data["client_type"]

    user_id = await database.get_user_id(user_code, client_type)

    if user_id:
        cart_id = await database.get_cart_id(user_id)
        return web.json_response({"cart_id": cart_id})
    else:
        user_id = await database.insert_into_users(user_code, client_type)
        cart_id = await database.insert_into_carts(user_id)
        return web.json_response({"cart_id": cart_id})


@routes.post('/add_item_to_cart')
async def add_item_to_cart(request):
    request_data = await request.json()

    cart_id = request_data["cart_id"]
    product_id = request_data["product_id"]
    quantity = int(request_data["quantity"])

    cart_item_id = await database.get_cart_item_id(cart_id=cart_id,
                                                   product_id=product_id)

    if cart_item_id:
        await database.update_cart_item(cart_item_id=cart_item_id,
                                        quantity=quantity)
        return web.Response(text="success")
    else:
        await database.insert_into_carts_items(cart_id=cart_id,
                                               product_id=product_id,
                                               quantity=quantity)
        return web.Response(text="success")


@routes.post('/get_cart_items')
async def get_cart_items(request):
    cart_id = await request.json()
    cart_items = await database.get_cart_items(cart_id["cart_id"])
    return web.json_response(cart_items)


@routes.post('/delete_item_from_cart')
async def delete_item_from_cart(request):
    request_data = await request.json()
    cart_id = request_data["cart_id"]
    product_id = request_data["product_id"]
    await database.delete_item_from_cart(cart_id, product_id)
    return web.Response(text="success")


@routes.post('/get_user_info')
async def get_user_info(request):
    request_data = await request.json()
    user_code = str(request_data["user_code"])
    client_type = request_data["client_type"]
    user_info = await database.select_user(user_code, client_type)
    return web.json_response(user_info)


@routes.post('/add_user_info')
async def add_user_info(request):
    request_data = await request.json()
    user_code = str(request_data["user_code"])
    client_type = request_data["client_type"]
    name = request_data["name"]
    phone = request_data["phone"]
    address = request_data["address"]

    # TODO Add phone, name, address processing
    await database.update_user_info(user_code=user_code,
                                    client_type=client_type,
                                    name=name,
                                    phone=phone,
                                    address=address)
    return web.Response(text="success")


@routes.post('/add_order')
async def add_order(request):
    # TODO add address to order table
    request_data = await request.json()
    cart_id = request_data["cart_id"]
    order_time = request_data["order_time"]

    user_id = await database.get_user_id_from_carts(cart_id)
    order_products = await database.get_cart_items(cart_id)

    order_products = [{"product_id": item["product_id"], 
                       "name": item["name"],
                       "quantity": item["quantity"]} for item in order_products]
    await database.insert_into_order(user_id=user_id, 
                                     order_time=order_time,
                                     order_products=order_products,
                                     cart_id=cart_id)

    await database.change_cart_status(cart_id=cart_id, status="order")
    await database.insert_into_carts(user_id)

    return web.Response(text="success")


@routes.post('/get_orders')
async def get_orders(request):
    request_data = await request.json()
    user_code = str(request_data["user_code"])
    client_type = request_data["client_type"]
    user_id = await database.get_user_id(user_code, client_type)

    user_orders = [{"order_id": order["order_id"],
                    "cart_id": order["cart_id"],
                    "tms_create": str(order["tms_create"]),
                    "order_time": order["order_time"]}
                    for order in await database.select_user_orders(user_id, "active")]
    return web.json_response(user_orders)


if __name__ == "__main__":
    # Add conn to db
    database = Database(user="vegetables",
                        database="vegetables",
                        host="vegetables-pg",
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
