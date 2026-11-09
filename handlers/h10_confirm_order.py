from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from bot_utils.counting_products import counting_products_from_cart
from config import ADMIN_ID
from database.utils import db_get_user_phone, db_save_order_history, db_clear_final_cart

router = Router()

@router.callback_query(F.data == 'confirm_orders')
async def confirm_order(callback: CallbackQuery, bot: Bot):
    """подтверждение заказоы"""
    user = callback.from_user
    phone = db_get_user_phone(user.id)
    mention = f"<a href=\"https://t.me/{user.username}\">{user.username}</a>"
    user_text = f"Номер заказ от {mention}\nс номером телефона {phone}"
    context = counting_products_from_cart(user.id, user_text)

    if not context:
        await callback.message.edit_text("Корзина пуста. Выберите товар)")
        await callback.answer()
        return
    if not ADMIN_ID:
        await callback.message.edit_text("Менеджер не указан(")
        await callback.answer()
        return

    count,text,total_price,cart_id = context
    await bot.send_message(chat_id=ADMIN_ID, text=context,parse_mode="HTML")

    db_save_order_history(user.id)

    db_clear_final_cart(callback.from_user.id)

    await callback.message.edit_text("Ваш заказ оформлен✅. Для связи с менеджером воспользуйтесь настройками")
    await callback.answer("Заказ оформлен")

