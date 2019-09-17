import sqlalchemy as sa

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
