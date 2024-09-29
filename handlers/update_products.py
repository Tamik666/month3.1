import sqlite3
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class EditProducts(StatesGroup):
    for_field = State()
    for_new_value = State()
    for_photo = State()

def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_products():
    conn = get_db_connection()
    products = (conn.execute
        ("""
        SELECT * FROM products p
        INNER JOIN products_details pd ON p.product_id = pd.product_id
        INNER JOIN collection_products cp ON p.product_id = cp.product_id
        """).fetchall())
    conn.close()
    return products

def update_products_field(product_id,field_name, new_value):
    products_table = ["name_product", "size", "price", "product_id", "photo"]
    products_details_table = ["product_id", "category", "info_product"]
    collection_products_table = ["product_id", "collection"]

    conn = get_db_connection()

    try:
        if field_name in products_table:
            query = f"UPDATE products SET {field_name} = ? WHERE product_id = ?"
        elif field_name in products_details_table:
            query = f"UPDATE products_details SET {field_name} = ? WHERE product_id = ?"
        elif field_name in collection_products_table:
            query = f"UPDATE collection_products SET {field_name} = ? WHERE product_id = ?"
        else:
            raise ValueError(f"forbidden field: {field_name}")

        conn.execute(query, (new_value, product_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

async def start_sending_products(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    button = InlineKeyboardButton("Look",callback_data=f"show_all_updates")
    keyboard.add(button)

    await message.reply("Show all products", reply_markup=keyboard)

async def send_all_products(callback_query: types.CallbackQuery):
    products = fetch_all_products()
    if products:
        for product in products:
            keyboard = InlineKeyboardMarkup(resize_keyboard=True)
            button = InlineKeyboardButton("Edit",callback_data=f"edit_{product['product_id']}")
            keyboard.add(button)

            caption = (f"Name: {product['name_product']}\n"
                       f"Size: {product['size']}\n"
                       f"Category: {product['category']}\n"
                       f"Price: {product['price']}\n"
                       f"ID: {product['product_id']}\n"
                       f"Info: {product['info_product']}\n"
                       f"Collection: {product['collection']}\n")
            await callback_query.message.answer_photo(photo=product['photo'],
                                                      caption=caption,
                                                      reply_markup=keyboard)
    else:
        await callback_query.message.answer("No products found")

async def edit_product_callback(callback_query: types.CallbackQuery, state: FSMContext):
    product_id = callback_query.data.split('_')[1]

    await state.update_data(product_id=product_id)

    keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)

    name_button = InlineKeyboardButton(text="Name", callback_data="field_name_product")
    category_button = InlineKeyboardButton(text="Category", callback_data="field_category")
    price_button = InlineKeyboardButton(text="Price", callback_data="field_price")
    size_button = InlineKeyboardButton(text="Size", callback_data="field_size")
    photo_button = InlineKeyboardButton(text="Photo", callback_data="field_photo")
    info_button = InlineKeyboardButton(text="Product info", callback_data="field_info_product")

    keyboard.add(name_button, category_button, price_button, size_button, photo_button, info_button)

    await callback_query.message.answer('Choose product to edit:',
                                        reply_markup=keyboard)
    await EditProducts.for_field.set()


async def select_field_callback(callback_query: types.CallbackQuery, state: FSMContext):
    field_map = {
        "field_name_product": "Name",
        "field_category": "Category",
        "field_price": "Price",
        "field_size": "Size",
        "field_photo": "Photo",
        "field_info_product": "Product Info",
    }

    field = field_map.get(callback_query.data)

    if not field:
        await callback_query.message.answer('Invalid string')
        return

    await state.update_data(field=field)

    if field == 'photo':
        await callback_query.message.answer('Send new photo:')
        await EditProducts.for_photo.set()
    else:
        await callback_query.message.answer(f'Enter new value for string {field}:')
        await EditProducts.for_new_value.set()


async def set_new_value(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    product_id = user_data['product_id']
    field = user_data['field']
    new_value = message.text

    update_products_field(product_id, field, new_value)

    await message.answer(f'String {field} updated successfully!')
    await state.finish()


async def set_new_photo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    product_id = user_data['product_id']

    photo_id = message.photo[-1].file_id

    update_products_field(product_id, 'photo', photo_id)

    await message.answer('Photo updated successfully!')
    await state.finish()



def register_update_products_handler(dp: Dispatcher):
    dp.register_message_handler(start_sending_products,commands=["products_update"])
    dp.register_callback_query_handler(send_all_products,Text(equals=["show_all_updates"]))
    dp.register_callback_query_handler(edit_product_callback,Text(startswith="edit"),state="*")
    dp.register_callback_query_handler(select_field_callback,Text(startswith="field"),state=EditProducts.for_field)
    dp.register_message_handler(set_new_value, state=EditProducts.for_new_value)
    dp.register_message_handler(set_new_photo, content_types=['photo'], state=EditProducts.for_photo)


