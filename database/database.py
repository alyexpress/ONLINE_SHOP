from . import db_session, transactions
from .users import User
from .sellers import Seller
from .products import Product
from .transactions import Transaction

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


    def create_user(self, username:str, email:str, password:str, balance:float = 100000):
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
            hashed_password=hashed_password(password),
                        balance=balance)
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


    def create_seller(self, user_id:int, name:str, balance:float = 0):
        db_sess = self.create_session()

        if not db_sess.query(User).filter(User.id == user_id).first():
            self.success = False
            self.errors.append((0, "Пльзователь с этим id не найден."))
        if not 4 <= len(name) <= 25:
            self.success = False
            self.errors.append((0, "Ваш никнейм должен быть длинной от 4 до 25 символов."))
        if db_sess.query(Seller).filter(Seller.name == name).first() is not None:
            self.success = False
            self.errors.append((0, "Этот никнейм уже занят."))
        if not self.success: return None
        new_seller = Seller(user_id=user_id, name=name, balance=balance)
        db_sess.add(new_seller)
        db_sess.commit()
        return new_seller

    def create_product(self, seller_id=int, name=str, price=float, count=int, description=None):
        db_sess = self.create_session()

        if not db_sess.query(Seller).filter(Seller.id == seller_id).first():
            self.success = False
            self.errors.append((0, "Пльзователь с этим id не найден."))
        if not 2 <= len(name) <= 50:
            self.success = False
            self.errors.append((1, "Название продукта должно быть от 2 до 50 символов."))
        if price <= 0:
            self.success = False
            self.errors.append((2, "Цена продукта должна быть больше 0."))
        if count < 0:
            self.success = False
            self.errors.append((3, "Количество продукта не может быть меньше нуля."))
        if not self.success: return None
        new_product = Product(
            seller_id=seller_id,
            name=name,
            price=price,
            count=count,
            description=description
        )
        db_sess.add(new_product)
        db_sess.commit()
        return new_product

    def purchase(self, user:User, products:dict):
        db_sess = self.create_session()

        if not products:
            self.success = False
            self.errors.append((1, "Передан пустой список товаров"))
            return None

        transactions = []

        for product_id in products.keys():
            product = db_sess.query(Product).filter(Product.id == product_id).first()

            if product.count < 1:
                self.success = False
                self.errors.append((1, f"Товар {product_id} закончился."))

            amount = product.price * products[product_id]

            transactions.append(Transaction(
                transaction_type=1,
                from_id=user.id,
                to_id=product.seller_id,
                amount=amount,
                product_id=product_id,
                product=product
            ))

            # db_sess.add(transaction)
            # user.balance -= amount
            # product.seller.balance += amount
            # product.count -= products[product_id]

        total = sum(list(map(lambda x: x.amount, transactions)))
        if total > user.balance:
            self.success = False
            self.errors.append((0, "Недостаточно средств."))

        if not self.success: return None

        user = db_sess.merge(user)
        user.balance -= total

        for transaction in transactions:
            transaction.product.seller.balance += transaction.amount
            db_sess.add(transaction)

        db_sess.commit()
        return None

    def replenishment(self, user_id, amount):
        db_sess = self.create_session()

        if not amount.isdigit():
            self.errors.append((1, "ВВеденно не число"))

        user = db_sess.query(User).filter(User.id == user_id).first()
        user.balance += int(amount)
        db_sess.commit()
        return None









