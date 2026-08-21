from . import db_session
from .users import User
from .sellers import Seller
from .products import Product

from app.utils import hashed_password


class Database:
    def __init__(self, filename:str):
        db_session.global_init(filename)
        self.success, self.errors = True, []


    @staticmethod
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(user_id)


    def create_session(self):
        self.success, self.errors = True, []
        return db_session.create_session()


    def create_user(self, username:str, email:str, password:str):
        db_sess = self.create_session()

        # Input data validation
        if not 4 <= len(username) <= 25:
            self.errors.append((0, "Ваш никнейм должен быть длинной от 4 до 25 символов."))
        if db_sess.query(User).filter(User.username == username).first() is not None:
            self.errors.append((0, "Этот никнейм уже занят."))
        if db_sess.query(User).filter(User.email == email).first() is not None:
            self.errors.append((1, "Пользователь с этим email уже зарегестрирован."))
        if not 4 <= len(password) <= 25: self.errors.append(
            (2, "Ваш пароль должен быть длинной от 4 до 25 символов."))

        if self.errors: self.success = False
        if not self.success: return None

        # Creating new user & save
        new_user = User(email=email, username=username,
            hashed_password=hashed_password(password))
        db_sess.add(new_user)
        db_sess.commit()

        return self.load_user(new_user.id)


    def login_user(self, login:str, password:str):
        db_sess = self.create_session()

        # Getting user by email or username
        user = db_sess.query(User).filter(User.email == login
            if "@" in login else User.username == login).first()

        # Input data validation
        if user is None or not user.check_password(password):
            self.errors.append((0, "Неверный email или username или пароль"))
            self.success = False
            return None

        return user


    # def create_seller(self, user_id=int, name=str):
    #     self.clear_last_data()
    #     db_sess = db_session.create_session()
    #     if not db_sess.query(User).filter(User.id == user_id).first():
    #         self.success = False
    #         self.errors.append((0, "Пльзователь с этим id не найден."))
    #     if not 4 <= len(name) <= 25:
    #         self.success = False
    #         self.errors.append((0, "Ваш никнейм должен быть длинной от 4 до 25 символов."))
    #     if db_sess.query(Seller).filter(Seller.name == name).first() is not None:
    #         self.success = False
    #         self.errors.append((0, "Этот никнейм уже занят."))
    #     if not self.success: return None
    #     new_seller = Seller(user_id=user_id, name=name)
    #     db_sess.add(new_seller)
    #     db_sess.commit()
    #     return new_seller
    #
    # def create_product(self, seller_id=int, name=str, price=float, count=int, description=None):
    #     self.clear_last_data()
    #     db_sess = db_session.create_session()
    #     if not db_sess.query(Seller).filter(Seller.seller_id == seller_id).first():
    #         self.success = False
    #         self.errors.append((0, "Пльзователь с этим id не найден."))
    #     if not 2 <= len(name) <= 50:
    #         self.success = False
    #         self.errors.append((1, "Название продукта должно быть от 2 до 50 символов."))
    #     if price <= 0:
    #         self.success = False
    #         self.errors.append((2, "Цена продукта должна быть больше 0."))
    #     if count < 0:
    #         self.success = False
    #         self.errors.append((3, "Количество продукта не может быть меньше нуля."))
    #     if not self.success: return None
    #     new_product = Product(
    #         seller_id=seller_id,
    #         name=name,
    #         price=price,
    #         count=count,
    #         description=description
    #     )
    #     return new_product


