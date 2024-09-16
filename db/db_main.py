import sqlite3
from db import queries

db = sqlite3.connect("db/store.sqlite3")
cursor = db.cursor()

def sql_create():
    if db:
        print("Database successfully connected")

    cursor.execute(queries.CREATE_TABLE_PRODUCTS)
    cursor.execute(queries.CREATE_TABLE_PRODUCTS_DETAILS)
    db.commit()

def sql_insert_products(name_product, size, price, product_id, info_product, photo):
    cursor.execute(queries.INSERT_PRODUCTS_QUERY, (name_product, size, price, product_id, photo))
    db.commit()

def sql_insert_products_info(product_id, category, info_product):
    cursor.execute(queries.INSERT_PRODUCTS_DETAILS_QUERY, (product_id, category, info_product))
    db.commit()
