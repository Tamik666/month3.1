import logging
from aiogram import types, Dispatcher
from config import bot, admin

# Set up logging
logging.basicConfig(level=logging.INFO)

async def welcome_user(message: types.Message):
    for member in message.new_chat_members:
        await message.answer(f"Welcome, {member.first_name}\n"
                             f"Rules:\n"
                             f"*Don't spam\n"
                             f"That's all")

words = ["wool", "bastard", "cunt"]

async def filter_words(message: types.Message):
    message_text = message.text.lower()
    for word in words:
        if word in message_text:
            await message.answer(f"Don't swear! {message.from_user.first_name}")
            await message.delete()
            break

user_warnings = {}

async def user_warning(message: types.Message):
    if message.chat.type != "private":
        if message.from_user.id not in admin:
            await message.answer("you're not admin")
        elif not message.reply_to_message:
            await message.answer("you must reply to a message")
        else:
            user_id = message.reply_to_message.from_user.id
            user_name = message.reply_to_message.from_user.full_name
            user_warnings[user_id] = user_warnings.get(user_id, 0) + 1

            for Admin in admin:
                await bot.send_message(chat_id=Admin,
                                       text=f"{user_name} get notice! {user_warnings[user_id]}/3")
                if user_warnings[user_id] >= 3:
                    await bot.kick_chat_member(message.chat.id, user_id)
                    await bot.unban_chat_member(message.chat.id, user_id)

                    await bot.send_message(chat_id=message.chat.id,
                                           text=f"{user_name} was kicked!")

async def pin_message(message: types.Message):
    logging.info("Pin message handler triggered.")  # Debug log
    if message.chat.type != 'private':
        if message.reply_to_message:
            pin = message.reply_to_message
            try:
                await bot.pin_chat_message(message.chat.id, pin.message_id)
                await message.answer("Message pinned successfully!")
            except Exception as e:
                await message.answer(f"An error occurred: {e}")
                logging.error(f"Error occurred while pinning message: {e}")
        else:
            await message.answer("You must reply to a message to pin it.")
    else:
        await message.answer('This command works only in groups.')

def register_admin_group(dp: Dispatcher):
    dp.register_message_handler(welcome_user, content_types=[types.ContentType.NEW_CHAT_MEMBERS])
    dp.register_message_handler(user_warning, commands=['warn'])
    dp.register_message_handler(pin_message, text="!pin")
    dp.register_message_handler(filter_words)
