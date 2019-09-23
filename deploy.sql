
CREATE TABLE IF NOT EXISTS categories(
    category_id serial PRIMARY KEY,
    name text UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_category_id ON categories (category_id);


CREATE TABLE IF NOT EXISTS subcategories(
    subcategory_id serial PRIMARY KEY,
    name text UNIQUE,
    category_id int,
    CONSTRAINT category_id FOREIGN KEY (category_id)
        REFERENCES categories (category_id) MATCH SIMPLE
);

CREATE INDEX IF NOT EXISTS idx_subcategory_id ON subcategories (subcategory_id);
CREATE INDEX IF NOT EXISTS idx_category_id_products ON subcategories (category_id);


CREATE TABLE IF NOT EXISTS products(
    product_id serial PRIMARY KEY,
    name text UNIQUE,
    cost integer,
    subcategory_id integer,
    photo text,
    CONSTRAINT subcategory_id FOREIGN KEY (subcategory_id)
        REFERENCES subcategories (subcategory_id) MATCH SIMPLE

);

CREATE INDEX IF NOT EXISTS idx_product_id ON products (product_id);
CREATE INDEX IF NOT EXISTS idx_subcategory_id_products ON products (subcategory_id);


CREATE TABLE IF NOT EXISTS users(
    user_id serial PRIMARY KEY,
    name text,
    phone text,
    address text,
    tms_create timestamp without time zone
);

CREATE INDEX IF NOT EXISTS idx_user_id ON users (user_id);


CREATE TABLE IF NOT EXISTS carts(
    cart_id serial PRIMARY KEY,
    user_id integer UNIQUE,
    tms_create timestamp without time zone,
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES users (user_id) MATCH SIMPLE
);

CREATE INDEX IF NOT EXISTS idx_cart_id ON carts (cart_id);
CREATE INDEX IF NOT EXISTS idx_user_id_carts ON carts (user_id);


CREATE TABLE IF NOT EXISTS carts_items(
    cart_item_id serial PRIMARY KEY,
    quantity integer,
    cart_id integer UNIQUE,
    product_id integer,
    CONSTRAINT cart_id FOREIGN KEY (cart_id)
        REFERENCES carts (cart_id) MATCH SIMPLE,
    CONSTRAINT product_id FOREIGN KEY (product_id)
        REFERENCES products (product_id) MATCH SIMPLE
);

CREATE INDEX IF NOT EXISTS idx_cart_item_id ON carts_items (cart_item_id);
CREATE INDEX IF NOT EXISTS idx_cart_id_carts_items ON carts_items (cart_id);
CREATE INDEX IF NOT EXISTS idx_product_id_carts_items ON carts_items (product_id);
