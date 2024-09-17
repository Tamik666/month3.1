from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
import buttons

class FSM_reg(StatesGroup):
    fullname = State()
    date = State()
    email = State()
    phone = State()
    address = State()
    gender = State()
    country = State()
    photo = State()
    submit = State()

async def start_fsm_reg(message: types.Message):
    await message.answer("Enter your full name:", reply_markup=buttons.cancel_button)
    await FSM_reg.fullname.set()

async def load_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text
    await message.answer('Enter your date of birth:')
    await FSM_reg.next()

async def load_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await message.answer('Enter your email:')
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
    await message.answer('Enter your gender:')
    await FSM_reg.next()

async def load_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await message.answer('Enter your country:')
    await FSM_reg.next()

async def load_country(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['country'] = message.text
    await message.answer('Please send your photo:')
    await FSM_reg.next()

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    await message.answer_photo(photo=data["photo"],
                               caption=f"Name: {data['fullname']}\n"
                                       f"Date of birth: {data['date']}\n"
                                       f"Email: {data['email']}\n"
                                       f"Phone number: {data['phone']}\n"
                                       f"Address: {data['address']}\n"
                                       f"Gender: {data['gender']}\n"
                                       f"Country: {data['country']}",
                               reply_markup=buttons.submit_button)
    await FSM_reg.submit.set()

async def submit(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardRemove()

    if message.text.lower() == "yes":
        await message.answer("Registration successful!", reply_markup=kb)
        await state.finish()

    elif message.text.lower() == "no":
        await message.answer("Registration aborted!", reply_markup=kb)
        await state.finish()

    else:
        await message.answer("Invalid input! Please type 'yes' or 'no'.")

async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is not None:
        await state.finish()
        await message.answer("Registration aborted!", reply_markup=ReplyKeyboardRemove())


def register_fsm_reg(dp: Dispatcher):
    dp.register_message_handler(cancel, Text(equals="Cancel", ignore_case=True), state="*")
    dp.register_message_handler(start_fsm_reg, commands=['reg'])
    dp.register_message_handler(load_fullname, state=FSM_reg.fullname)
    dp.register_message_handler(load_date, state=FSM_reg.date)
    dp.register_message_handler(load_email, state=FSM_reg.email)
    dp.register_message_handler(load_phone, state=FSM_reg.phone)
    dp.register_message_handler(load_address, state=FSM_reg.address)
    dp.register_message_handler(load_gender, state=FSM_reg.gender)
    dp.register_message_handler(load_country, state=FSM_reg.country)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSM_reg.photo)
    dp.register_message_handler(submit, state=FSM_reg.submit)