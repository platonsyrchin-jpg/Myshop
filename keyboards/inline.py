from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.utils import db_get_all_category


def create_category_menu(chat_id):
    """Предоставление меню с категориями товаров"""
    categories = db_get_all_category()
    total_price = db_get_finally_price(chat_id)

    builder = InlineKeyboardBuilder()
    builder.button(text=f"Корзина заказа ({total_price if total_price else 0})₽",
                   callback_data = "корзина заказа"
                   )
    [builder.button(text=category.category_name, callback_data = f"category_{category.id}") for category in categories]

    builder.adjust(1,2)
    return builder.as_markup()