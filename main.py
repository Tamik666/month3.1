import logging

logging.basicConfig(level=logging.INFO)


from aiogram.utils import executor
from buttons import start, start_test
from config import bot, dp, admin
from handlers import (commands, echo, quiz, FSM_registration,FSM_store,webapp,admin_group,send_products,
                      send_delete_products,update_products)
from db import db_main


async def on_startup(_):
    for i in admin:
        await bot.send_message(chat_id=i, text="Bot is ready!", reply_markup=start_test)

        db_main.sql_create()

commands.register_commands(dp)
quiz.register_quiz(dp)
FSM_registration.register_fsm_reg(dp)
FSM_store.register_fsm_store(dp)
webapp.register_handlers_webapp(dp)
send_products.register_send_products(dp)
send_delete_products.register_send_deleted_products(dp)
update_products.register_update_products_handler(dp)
admin_group.register_admin_group(dp)
# echo.register_echo(dp)




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)