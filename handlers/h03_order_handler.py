from aiogram import Router, F, Bot
from aiogram.types import Message

from database.utils import db_get_last_orders
from keyboards.inline import create_category_menu
from keyboards.reply import back_to_main_menu

router = Router()

@router.message(F.text == "Оформить заказ🛍")
async def make_order(message: Message, bot: Bot):
    """оформление заказа, кнопка перехода в меню заказа"""
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id,text="Формируем заказ:", reply_markup=back_to_main_menu())
    await message.answer(text="Выберете категорию", reply_markup=create_category_menu(chat_id))


@router.message(F.text == "История🕒")
async def make_history(message: Message):
    """Обработка истории заказа"""
    chat_id = message.chat.id
    orders = db_get_last_orders(chat_id)

    if not orders:
        await message.answer(text="У вас нет истории заказов😥")
        return

    text = "Ваша история:\n\n"
    for order in orders:
        text += f"{order.product_name} - {order.final_price} руб. - {order.quantity} шт.\n"
    await message.answer(text=text)


