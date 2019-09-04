
CREATE TABLE IF NOT EXISTS kingdoms(
    kingdom_id serial PRIMARY KEY,
    name text UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_kingdom_id ON kingdoms (kingdom_id);


CREATE TABLE IF NOT EXISTS categories(
    category_id serial PRIMARY KEY,
    name text UNIQUE,
    kingdom_id int,
    CONSTRAINT kingdom_id FOREIGN KEY (kingdom_id)
        REFERENCES kingdoms (kingdom_id) MATCH SIMPLE
);

CREATE INDEX IF NOT EXISTS idx_category_id ON categories (category_id);
CREATE INDEX IF NOT EXISTS idx_kingdom_id_products ON categories (kingdom_id);


CREATE TABLE IF NOT EXISTS products(
    product_id serial PRIMARY KEY,
    name text UNIQUE,
    cost integer,
    category_id integer,
    photo text,
    CONSTRAINT category_id FOREIGN KEY (category_id)
        REFERENCES categories (category_id) MATCH SIMPLE

);

CREATE INDEX IF NOT EXISTS idx_product_id ON products (product_id);
CREATE INDEX IF NOT EXISTS idx_category_id_products ON products (category_id);
