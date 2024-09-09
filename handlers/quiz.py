from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot


async def quiz_1(message: types.Message):
    quiz_button = InlineKeyboardMarkup()
    button_quiz_1 = InlineKeyboardButton('Next...', callback_data="button_2")
    quiz_button.add(button_quiz_1)

    question = 'BMW or Mercedes?'
    answer = ['BMW', 'Mercedes', 'Lada']

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        explanation='Deutchland',
        open_period=60,
        reply_markup=quiz_button
    )

async def quiz_2(call: types.CallbackQuery):
    quiz_button2 = InlineKeyboardMarkup()
    button_quiz_2 = InlineKeyboardButton('Next...', callback_data='button_3')
    quiz_button2.add(button_quiz_2)

    question = 'Back or Front'
    answer = ['Back', 'Frond', 'Design']

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        explanation='(((',
        open_period=60,
        reply_markup=quiz_button2
    )


async def quiz_3(call: types.CallbackQuery):
    question = "PC or PS4"
    answer = ["PC", "PS4"]

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        explanation='(((',
        open_period=60,
    )


def register_quiz(dp: Dispatcher):
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, text=["button_2"])
    dp.register_callback_query_handler(quiz_3, text=["button_3"])