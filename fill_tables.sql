INSERT INTO "kingdoms"(kingdom_id, name) VALUES (1, 'Грибы');
INSERT INTO "kingdoms"(kingdom_id, name) VALUES (2, 'Зелень');
INSERT INTO "kingdoms"(kingdom_id, name) VALUES (3, 'Овощи');
INSERT INTO "kingdoms"(kingdom_id, name) VALUES (4, 'Фрукты');

INSERT INTO "categories"(category_id, name, kingdom_id) VALUES (1, 'Шампиньоны', 1);
INSERT INTO "categories"(category_id, name, kingdom_id) VALUES (2, 'Баклажан', 3);
INSERT INTO "categories"(category_id, name, kingdom_id) VALUES (3, 'Лук', 3);
INSERT INTO "categories"(category_id, name, kingdom_id) VALUES (4, 'Огурцы', 3);

INSERT INTO "products"(product_id, name, cost, category_id, photo) VALUES (1, 'Шампиньоны 1', 25, 1, '/photo/1');
INSERT INTO "products"(product_id, name, cost, category_id, photo) VALUES (2, 'Баклажан 1 ', 25, 2, '/photo/1');
INSERT INTO "products"(product_id, name, cost, category_id, photo) VALUES (3, 'Лук 1', 25, 3, '/photo/1');
INSERT INTO "products"(product_id, name, cost, category_id, photo) VALUES (4, 'Лук 2', 25, 3, '/photo/1');
