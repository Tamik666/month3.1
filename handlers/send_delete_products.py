import sqlite3
from urllib.request import urlopen

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from aiogram.dispatcher.filters import Text
from config import admin, bot

def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
    SELECT * FROM products p
    INNER JOIN products_details pd ON p.product_id = pd.product_id
    INNER JOIN collection_products cp ON p.product_id = cp.product_id"""
    ).fetchall()
    conn.close()
    return products

def delete_all_products(product_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
    conn.execute("DELETE FROM products_details WHERE product_id = ?", (product_id,))
    conn.execute("DELETE FROM collection_products WHERE product_id = ?", (product_id,))
    conn.commit()
    conn.close()

async def start_sending(message: types.Message):
    if message.chat.type != "private":
        if message.from_user.id not in admin:
            await message.answer("you're not admin")
        else:
            keyboard = InlineKeyboardMarkup(resize_keyboard=True)

            button = InlineKeyboardButton("All goods", callback_data="show_all_delete")
            keyboard.add(button)

            await message.answer("Press to delete all goods", reply_markup=keyboard)

async def send_deleted_products(callback_query: types.CallbackQuery):
    if callback_query.from_user.id not in admin:
        await callback_query.answer("you're not admin")
        return
    else:
        products = fetch_all_products()
        if products:
            for product in products:
                caption = (f"Name: {product['name_product']}\n"
                           f"Size: {product['size']}\n"
                           f"Category: {product['category']}\n"
                           f"Price: {product['price']}\n"
                           f"ID: {product['product_id']}\n"
                           f"Info: {product['info_product']}\n"
                           f"Collection: {product['collection']}\n")
                delete_products_markup = InlineKeyboardMarkup(resize_keyboard=True)
                delete_products_button = InlineKeyboardButton("Delete", callback_data=f"delete_{product['product_id']}")
                delete_products_markup.add(delete_products_button)
                await callback_query.message.answer_photo(photo=product["photo"], caption=caption, reply_markup=delete_products_markup)
        else:
            await callback_query.message.answer("No products found")

async def delete_products_callback(callback_query: types.CallbackQuery):
    if callback_query.from_user.id not in admin:
        await callback_query.answer("you're not admin")
        return
    product_id = callback_query.data.split("_")[1]

    delete_all_products(product_id)

    if callback_query.message.photo:
        new_caption = f"Product deleted\nRefresh list."

        photo404 = open("media/404.jpg", "rb")

        await callback_query.message.edit_media(InputMediaPhoto(media=photo404, caption=new_caption))
    else:
        await callback_query.message.answer("Product deleted.")

def register_send_deleted_products(dp: Dispatcher):
    dp.register_message_handler(start_sending, commands=["delete"])
    dp.register_callback_query_handler(send_deleted_products, Text(equals="show_all_delete"))
    dp.register_callback_query_handler(delete_products_callback, Text(startswith="delete_"))
