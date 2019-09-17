
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
