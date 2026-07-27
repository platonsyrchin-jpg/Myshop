from aiogram import Router, F, Bot
from aiogram.types import Message

from keyboards.inline import create_category_menu

router = Router()

@router.message(F.text == "Оформить заказ🛍")
async def make_order(message: Message, bot: Bot):
    """оформление заказа, кнопка перехода в меню заказа"""
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id,text="Сделайте выбор товара:", reply_markup=back_to_main_menu())
    await message.answer(text="Выберете категорию", reply_markup=create_category_menu(chat_id))
