from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineQueryResultArticle, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot_utils.cart_text import generate_cart_text
from database.utils import db_get_product_for_delete, db_increase_product_quantity, db_get_cart_items

router = Router()

@router.callback_query(F.data == 'choose_to_add')
async def choose_product_to_add(callback: CallbackQuery):
    """Выбор товара для добавления"""
    chat_id = callback.from_user.id
    cart_products = db_get_product_for_delete(chat_id)
    builder = InlineKeyboardBuilder()
    for cart_id, name in cart_products:
        builder.button(text=f'➕ {name}', callback_data=f'increase_{cart_id}')
    builder.button(text='Назад🔙', callback_data='back_to_cart_review')
    builder.adjust(1)

    await callback.message.edit_text(text='Выберите товар для увеличения количества:',
                                     reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == 'choose_to_remove')
async def choose_product_to_remove(callback: CallbackQuery):
    """Выбор товара для удаления"""
    chat_id = callback.from_user.id
    cart_products = db_get_product_for_delete(chat_id)
    builder = InlineKeyboardBuilder()
    for cart_id, name in cart_products:
        builder.button(text=f'➖ {name}', callback_data=f'decrease_{cart_id}')
    builder .button(text='Назад🔙', callback_data='back_to_cart_review')
    builder.adjust(1)

    await callback.message.edit_text(text='Выберите товар для уменьшение количества:',
                                     reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith('increase_'))
async def increase_quantity(callback: CallbackQuery):
    """Обработка кнопки увеличения количества"""
    cart_id = int(callback.data.split('_')[1])
    db_increase_product_quantity(cart_id)

    user_id = callback.from_user.id
    cart_items = db_get_cart_items(user_id)
    text = generate_cart_text(cart_items)

    builder = InlineKeyboardBuilder()
    builder.button(text='Назад🔙', callback_data='back_to_cart_review')
    builder.button(text='+ Добавить кол-во', callback_data=f'increase_{cart_id}')
    builder.adjust(1)
    await callback.message.edit_text(text=text,
                                     reply_markup=builder.as_markup())
    await callback.answer('Количество увеличено⬆')

@router.callback_query(F.data.startswith('decrease_'))
async def decrease_quantity(callback: CallbackQuery, bot: Bot):
    pass