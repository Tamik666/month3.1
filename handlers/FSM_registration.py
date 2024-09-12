from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

class FSM_reg(StatesGroup):
    fullname = State()
    date = State()
    email = State()
    phone = State()
    address = State()
    gender = State()
    country = State()
    photo = State()

async def start_fsm_reg(message: types.Message):
    await message.answer("Enter your fullname")
    await FSM_reg.fullname.set()

async def load_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text
    await message.answer('Enter date of birth: ')
    await FSM_reg.next()

async def load_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await message.answer('Enter your email ')
    await FSM_reg.next()

async def load_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    await message.answer('Enter your phone number:')
    await FSM_reg.next()

async def load_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await message.answer('Enter your address:')
    await FSM_reg.next()

async def load_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await message.answer('Gender:')
    await FSM_reg.next()

async def load_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await message.answer('Enter your country:')
    await FSM_reg.next()

async def load_country(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['country'] = message.text
    await message.answer('Send your photo:')
    await FSM_reg.next()


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    await message.answer('Registration successful!')
    # Выводим все данные пользователю
    await message.answer_photo(photo=data["photo"],
                 caption=f"Name: {data['fullname']}\n\n"
                         f"Date of birth: {data['date']}\n"
                         f"Email: {data['email']}\n"
                         f"Number: {data['phone']}\n"
                         f"Address: {data['address']}\n"
                         f"Gender: {data['gender']}\n"
                         f"Country: {data['country']}")

    await state.finish()


def register_fsm_reg(dp: Dispatcher):
    dp.register_message_handler(start_fsm_reg, commands=['reg'])
    dp.register_message_handler(load_fullname,state=FSM_reg.fullname)
    dp.register_message_handler(load_date,state=FSM_reg.date)
    dp.register_message_handler(load_email, state=FSM_reg.email)
    dp.register_message_handler(load_phone, state=FSM_reg.phone)
    dp.register_message_handler(load_address, state=FSM_reg.address)
    dp.register_message_handler(load_gender, state=FSM_reg.gender)
    dp.register_message_handler(load_country, state=FSM_reg.country)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSM_reg.photo)

#-----------------------------------------------------------------------------------------------------------------------

class FSM_store(StatesGroup):
    product_name = State()
    size = State()
    category = State()
    price = State()
    photo = State()


async def start_fsm_store(message: types.Message):
    await message.answer("Goods name:")
    await FSM_store.product_name.set()


# Обработка названия товара
async def load_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_name'] = message.text
    await message.answer('Choose sizes:')

    # Создаем кнопки для выбора размера
    size_buttons = InlineKeyboardMarkup(row_width=3)
    sizes = ['S', 'M', 'L', 'XL', 'XXL', '3XL']
    size_buttons.add(*[InlineKeyboardButton(size, callback_data=size) for size in sizes])

    await FSM_store.next()
    await message.answer("Choose sizes:", reply_markup=size_buttons)


# Обработка выбора размера через callback
async def load_size(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = callback_query.data
    await callback_query.message.answer('Category:', reply_markup=ReplyKeyboardRemove())
    await FSM_store.next()


# Обработка категории товара
async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await message.answer('Price:')
    await FSM_store.next()


# Обработка стоимости товара
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Goods Photo:')
    await FSM_store.next()


# Обработка фото товара
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    # Подтверждение регистрации товара
    await message.answer("Goods successfully added!")

    # Отправка фотографии товара и данных
    await message.answer_photo(photo=data['photo'],
                               caption=f"Name: {data['product_name']}\n"
                                       f"Size: {data['size']}\n"
                                       f"Category: {data['category']}\n"
                                       f"Price: {data['price']}")

    await state.finish()


# Регистрация всех обработчиков
def register_fsm_store(dp: Dispatcher):
    dp.register_message_handler(start_fsm_store, commands=['store'])
    dp.register_message_handler(load_product_name, state=FSM_store.product_name)
    dp.register_callback_query_handler(load_size, state=FSM_store.size)
    dp.register_message_handler(load_category, state=FSM_store.category)
    dp.register_message_handler(load_price, state=FSM_store.price)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSM_store.photo)