from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton


async def reply_webapp(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,row_width=2)

    geeks_online = KeyboardButton("Geeks Online", web_app=types.WebAppInfo(url="https://online.geeks.kg/"))
    youtube = KeyboardButton(text="YouTube", web_app=types.WebAppInfo(url="https://www.youtube.com/"))
    github = KeyboardButton("GitHub", web_app=types.WebAppInfo(url="https://github.com/"))
    google = KeyboardButton("Google", web_app=types.WebAppInfo(url="https://google.com/"))
    instagram = KeyboardButton("Instagram", web_app=types.WebAppInfo(url="https://instagram.com/"))

    keyboard.add(geeks_online, youtube, github, google, instagram)

    await message.answer(text="WebApp buttons: ", reply_markup=keyboard)

async def inline_webapp(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)

    chatgpt = InlineKeyboardButton("chatgpt", web_app=types.WebAppInfo(url="https://chatgpt.com/?oai-dm=1"))

    keyboard.add(chatgpt)

    await message.answer(text="Inline buttons: ", reply_markup=keyboard)

def register_handlers_webapp(dp:Dispatcher):
    dp.register_message_handler(reply_webapp,commands=["reply_webapp"])
    dp.register_message_handler(inline_webapp,commands=["inline_webapp"])
