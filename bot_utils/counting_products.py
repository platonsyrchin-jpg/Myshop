from database.utils import db_get_cart_items

def counting_products_from_cart(chat_id, user_text):
    """подсчёт товаров из корзины и формирование описания"""
    items = db_get_cart_items()
    if not items:
        return None

    text = f'{user_text}</b>\n '
    total_products = 0
    total_price = 0
    count = 0
    cart_id = None

    for idx, item in enumerate(items, start=1):
        name = item['product_name']
        qty = item['quantity']
        price = float(item['final_price'])

        item_total = price
        total_price += item_total
        total_products += qty
        count += 1
        cart_id = item['product_id']

        text += f'<b>{idx}:{name}</b>\n '
        text += f'<b>quantity:{qty}</b>\n '
        text += f'<b>price:{item_total:.2f} ₽</b>\n '

    text += (f'<b>products quantity:{total_products}</b>\n '
    f'<b>all items price:{total_products}</b>\n ')
    return count, text, total_price, cart_id
