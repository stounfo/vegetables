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
    user_code text,
    client_type text,
    name text,
    phone text,
    address text,
    tms_create timestamp without time zone,
    UNIQUE (user_code, client_type)
);

CREATE INDEX IF NOT EXISTS idx_user_id_users ON users (user_id);
CREATE INDEX IF NOT EXISTS idx_user_code_users ON users (user_code);
CREATE INDEX IF NOT EXISTS idx_client_type_users ON users (client_type);


CREATE TABLE IF NOT EXISTS carts(
    cart_id serial PRIMARY KEY,
    user_id integer UNIQUE,
    tms_create timestamp without time zone,
    status text,
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES users (user_id) MATCH SIMPLE
);

CREATE INDEX IF NOT EXISTS idx_cart_id ON carts (cart_id);
CREATE INDEX IF NOT EXISTS idx_user_id_carts ON carts (user_id);
CREATE INDEX IF NOT EXISTS idx_status_carts ON carts (status);


CREATE TABLE IF NOT EXISTS carts_items(
    cart_item_id serial PRIMARY KEY,
    quantity integer,
    cart_id integer,
    product_id integer,
    UNIQUE (cart_id, product_id),
    CONSTRAINT cart_id FOREIGN KEY (cart_id)
        REFERENCES carts (cart_id) MATCH SIMPLE,
    CONSTRAINT product_id FOREIGN KEY (product_id)
        REFERENCES products (product_id) MATCH SIMPLE
);

CREATE INDEX IF NOT EXISTS idx_cart_item_id ON carts_items (cart_item_id);
CREATE INDEX IF NOT EXISTS idx_cart_id_carts_items ON carts_items (cart_id);
CREATE INDEX IF NOT EXISTS idx_product_id_carts_items ON carts_items (product_id);


CREATE TABLE IF NOT EXISTS orders(
    order_id serial PRIMARY KEY,
    tms_create timestamp without time zone,
    user_id integer,
    order_time text,
    order_products JSONB,
    cart_id integer UNIQUE,
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES users (user_id) MATCH SIMPLE,
    CONSTRAINT cart_id FOREIGN KEY (cart_id)
        REFERENCES carts (cart_id) MATCH SIMPLE
);

CREATE INDEX IF NOT EXISTS idx_order_id ON orders (order_id);
CREATE INDEX IF NOT EXISTS idx_user_id_orders ON orders (user_id);
