from aiogram import types, Dispatcher

async def echo_handler(message: types.Message):
    if message.text.isdigit():
        number = int(message.text)
        result = number ** 2
        await message.answer(f"{result}")
    else:
        await message.answer(message.text)

def register_echo(dp: Dispatcher):
    dp.register_message_handler(echo_handler)