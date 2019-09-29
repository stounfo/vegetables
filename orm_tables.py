import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

categories = sa.Table("categories", sa.MetaData(),
                    sa.Column("category_id", sa.Integer, primary_key=True),
                    sa.Column("name", sa.String))


subcategories = sa.Table("subcategories", sa.MetaData(),
                    sa.Column("subcategory_id", sa.Integer, primary_key=True),
                    sa.Column("name", sa.String),
                    sa.Column("category_id", sa.Integer))


products = sa.Table("products", sa.MetaData(),
                    sa.Column("product_id", sa.Integer, primary_key=True),
                    sa.Column("name", sa.String),
                    sa.Column("cost", sa.Integer),
                    sa.Column("subcategory_id", sa.Integer),
                    sa.Column("photo", sa.String))


users = sa.Table("users", sa.MetaData(),
                    sa.Column("user_id", sa.Integer, primary_key=True),
                    sa.Column("user_code", sa.String),
                    sa.Column("client_type", sa.String),
                    sa.Column("name", sa.String),
                    sa.Column("phone", sa.String),
                    sa.Column("address", sa.String),
                    sa.Column("tms_create", sa.DateTime))


carts = sa.Table("carts", sa.MetaData(),
                    sa.Column("cart_id", sa.Integer, primary_key=True),
                    sa.Column("user_id", sa.Integer),
                    sa.Column("tms_create", sa.DateTime),
                    sa.Column("status", sa.String),)


carts_items = sa.Table("carts_items", sa.MetaData(),
                    sa.Column("cart_item_id", sa.Integer, primary_key=True),
                    sa.Column("quantity", sa.Integer),
                    sa.Column("cart_id", sa.Integer),
                    sa.Column("product_id", sa.Integer))
        

orders = sa.Table("orders", sa.MetaData(),
                    sa.Column("order_id", sa.Integer, primary_key=True),
                    sa.Column("tms_create", sa.DateTime),
                    sa.Column("user_id", sa.Integer),
                    sa.Column("order_time", sa.String),
                    sa.Column("order_products", JSONB),
                    sa.Column("cart_id", sa.Integer))
