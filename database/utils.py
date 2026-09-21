from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from database.base import engine
from sqlalchemy import update, select, join
from database.models import (Users, Products, Carts, Orders, Categories, FinallyCarts)


def get_session():
    return Session(engine)


def db_register_user(full_name: str, chat_id: int):
    """Регистрация юзера в базе"""

    try:
        with get_session() as session:
            query = Users(name=full_name, telegram=chat_id)
            session.add(query)
            session.commit()
        return False
    except IntegrityError:
        return True


def db_update_user(chat_id: int, phone: str):
    """получение номера телефона пользователя, обновляем данные у пользователя"""
    with get_session() as session:
        query = update(Users).where(Users.telegram == chat_id).values(phone=phone)
        session.execute(query)
        session.commit()


def db_create_user_cart(chat_id: int):
    """Создание корзины пользователя после регистрации"""
    try:
        with get_session() as session:
            subquery = session.scalar(select(Users).where(Users.telegram == chat_id))
            query = Carts(user_id=subquery.id)
            session.add(query)
            session.commit()
            return True
    except IntegrityError:
        return False


def db_get_all_category():
    """получение всех категорий"""
    with get_session() as session:
        query = select(Categories)
        return session.scalars(query).all()


def db_get_finally_price(chat_id):
    """получение итоговой цены"""
    with get_session() as session:
        query = select(func.sum(FinallyCarts.final_price)).select_from(
            join(Carts, FinallyCarts, Carts.id == FinallyCarts.cart_id)).join(Users, Users.id == Carts.user_id).where(
            Users.telegram == chat_id)
        return session.execute(query).fetchone()[0]


def db_get_last_orders(chat_id, limit=5):
    """Получение истории заказов"""
    with get_session() as session:
        query = (
            select(Orders),
            join(Carts, Orders.cart_id == Carts.id).
            join(Users, Users.id == Carts.user_id).
            where(Users.telegram == chat_id).
            order_by(Orders.id.desc()).
            limit(limit)
        )
        return session.scalars(query).all()

def db_get_products(category_id):
    """Получение продуктов по id категории"""
    with get_session() as session:
        query = select(Products).where(Products.category_id == category_id)
        return session.scalars(query).all()

def db_get_products_by_id(product_id):
    """Получение продуктов поих ID"""
    with get_session() as session:
        query = select(Products).where(Products.id == product_id)
        return session.scalar(query)

def db_get_user_cart(chat_id):
    """Получение корзины пользователя по его ID"""
    with get_session() as session:
        query = select(Carts).join(Users).where(Users.telegram == chat_id)
        return session.scalar(query)

def db_add_or_update_item(
        cart_id: int,
        product_id: int,
        product_name: str,
        product_price: DECIMAL,
        increment: int = 0):
    """Добавление или изменение товара"""
    try:
        with get_session() as session:
            item = (session.query(FinallyCarts)
                    .filter_by(cart_id=cart_id, product_id=product_id)
                    .first())
            if item:
                if increment != 0:
                    item.quantity = max(1, item.quantity + increment)
                else:
                    qty = 1 if increment <= 0 else increment
                    item = FinallyCarts(
                        cart_id=cart_id,
                        product_id=product_id,
                        product_name=product_name,
                        quantity=qty,
                        final_price=0
                    )
                    session.add(item)

                item.final_price = item.quantity * product_price

                products_sum, total_products = session.query(
                    func.coalesce(func.sum(FinallyCarts.final_price), 0),
                    func.coalesce(func.sum(FinallyCarts.quantity), 0),
                ).filter(
                    FinallyCarts.cart_id == cart_id,
                ).one()

                session.query(Carts).filter(
                    Carts.id == cart_id
                ).update({
                    Carts.total_price: products_sum,
                    Carts.total_products: total_products
                })
                session.commit()

                return {
                    "status":"ok",
                    "total_price": float(products_sum),
                    "total_products": int(total_products),
                    "products_quantity": item.quantity,
                }
    except Exception as e:
        print(e)
        return {"status": "error"}






