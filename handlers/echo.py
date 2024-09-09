from pyexpat.errors import messages
from config import bot
from aiogram import types, Dispatcher
import random
games = ['⚽', '🎰', '🏀', '🎯', '🎳', '🎲']
async def echo_handler(message: types.Message):
    if message.text.isdigit():
        number = int(message.text)
        result = number ** 2
        await message.answer(f"{result}")
    elif message.text == "game":
        random_game = random.choice(games)
        await bot.send_dice(
            chat_id=message.from_user.id,
            emoji=random_game)

        bot_dice = await bot.send_dice(chat_id=message.from_user.id, emoji='🎲')
        bot_result = bot_dice.dice.value

        player_dice = await message.answer_dice(emoji='🎲')
        player_result = player_dice.dice.value

        if bot_result > player_result:
            await message.answer("Bot wins!")
        elif bot_result < player_result:
            await message.answer("Player wins!")
        else:
            await message.answer("Draw!")
    else:
        await message.answer(message.text)
def register_echo(dp: Dispatcher):
    dp.register_message_handler(echo_handler)