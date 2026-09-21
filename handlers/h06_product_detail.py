from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardMarkup, chat

from bot_utils.message_utils import text_for_caption
from database.utils import db_get_products_by_id, db_get_user_cart, db_add_or_update_item
from keyboards.reply import phone_button

router = Router()


@router.callback_query(F.data.startswith("product_view"))
async def show_product_detail(callback: CallbackQuery, bot: Bot):
    """Показываем детали продукта"""

    chat_id = callback.message.chat.id
    message_id =  callback.message.message_id
    await bot.delete_message(chat_id, message_id)

    product_id = callback.data.split("_")[-1]
    product = db_get_products_by_id(product_id)

    user_cart = db_get_user_cart(chat_id)
    if user_cart:
        db_add_or_update_item(
            cart_id=user_cart.id,
            product_id=product.id,
            product_name=product.product_name,
            product_price=product.price,
            increment=1
        )
        caption = text_for_caption(
            name=product.product_name,
            description=product.description,
            base_price=float(product.price),
        )
        product_image = FSInputFile(path=product.image)

        await bot.send_photo(chat_id=chat_id,
                              photo=product_image,
                              caption=caption,
                              parse_mode="html",
                              reply_markup=quantity_cart_controls())

    else:
        await ask_for_phone(chat_id, bot)


async def ask_for_phone(chat_id: int, bot: Bot):
    """Запрос телефона при авторизации"""
    await bot.send_message(chat_id=chat_id, text="Предоставьте номер телефона для оформления заказа",
                           reply_markup=phone_button())

