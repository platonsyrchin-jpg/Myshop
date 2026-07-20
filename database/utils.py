from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database.base import engine
from sqlalchemy import update, select
from database.models import (Users,Products,Carts,Orders,Categories,FinallyCarts)


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