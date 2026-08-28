from .models import User, Seller, Product, Category, Transaction
from . import session

from datetime import datetime
from app.utils import hashed_password, get_cart_cookie, toRub


class Database:
    def __init__(self, filename:str):
        session.global_init(filename)
        self.success, self.errors = True, []


    @staticmethod
    def load_user(user_id):
        db_sess = session.create_session()
        return db_sess.query(User).get(user_id)


    def create_session(self):
        self.success, self.errors = True, []
        return session.create_session()


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


    def has_seller(self, user:User) -> bool:
        db_sess = self.create_session()
        return db_sess.query(Seller).filter(
            Seller.user_id == user.id).first() is not None


    def get_seller(self, user:User, cookie=None):
        db_sess = self.create_session()

        if cookie is None:
            return db_sess.query(Seller).filter(
                Seller.user_id == user.id).first()

        hash_password = cookie.get('seller', '')
        return db_sess.query(Seller).filter(Seller.user_id == user.id,
            Seller.hashed_password == hash_password).first()


    def create_seller(self, user:User, shop_name:str, password:str):
        db_sess = self.create_session()

        # Input data validation
        if not 4 <= len(shop_name) <= 25: self.errors.append(
            (0, "Название магазина должен быть длинной от 4 до 25 символов."))
        if not 4 <= len(password) <= 25: self.errors.append(
            (1, "Пароль должен быть длинной от 4 до 25 символов."))
        if db_sess.query(Seller).filter(Seller.shop_name == shop_name).first() is not None:
            self.errors.append((0, "Это название магазина уже занято."))

        if self.errors: self.success = False
        if not self.success: return None

        # Creating new Seller
        seller = Seller(user_id=user.id, shop_name=shop_name,
                        hashed_password=hashed_password(password))
        db_sess.add(seller)
        db_sess.commit()
        return db_sess.query(Seller).filter(Seller.id == seller.id).first()


    def login_seller(self, user:User, password:str):
        seller = self.get_seller(user)
        return seller if (seller.hashed_password ==
                hashed_password(password)) else None


    def create_product(self, seller_id:int, category_id:int, name:str, description:str,
                       img_src:str, price:float, count:int, discount_price:float=None):

        db_sess = self.create_session()

        if not 2 <= len(name) <= 100: self.errors.append(
            (1, "Название продукта должно быть от 2 до 100 символов."))
        if price <= 0 or (type(discount_price) is int and discount_price <= 0):
            self.errors.append((4, "Цена продукта должна быть больше 0."))
        if count < 0: self.errors.append(
            (5, "Количество продукта не может быть меньше нуля."))

        if self.errors: self.success = False
        if not self.success: return None

        new_product = Product(seller_id=seller_id, category_id=category_id,
            name=name, description=description, img_src=img_src, price=price,
            discount_price=discount_price, count=count)
        db_sess.add(new_product)
        db_sess.commit()

        return new_product


    def purchase(self, user:User, cookies):
        products = get_cart_cookie(cookies)
        db_sess = self.create_session()

        if not products:
            self.success = False
            self.errors.append((1, "Передан пустой список товаров"))
            return None

        transactions = []

        for product_id in products.keys():
            product = db_sess.query(Product).get(product_id)

            if product.count < products[product_id]:
                self.success = False
                self.errors.append((1, f"Товар {product_id} закончился."))
                return None

            price = product.discount_price if product.discount_price else product.price
            amount = price * products[product_id]

            transactions.append(Transaction(
                type=1,
                product_id=product_id,
                from_id=user.id,
                to_id=product.seller_id,
                amount=amount,
                product=product
            ))

        total = sum(list(map(lambda x: x.amount, transactions)))
        print(total)

        if total > user.balance:
            self.success = False
            self.errors.append((0, "Недостаточно средств."))
            return None

        user = db_sess.merge(user)
        user.balance -= total

        for transaction in transactions:
            transaction.product.count -= products[transaction.product_id]
            transaction.product.seller.balance += transaction.amount
            db_sess.add(transaction)

        db_sess.commit()


    def replenishment(self, user_id, amount):
        db_sess = self.create_session()

        if not amount.isdigit():
            self.errors.append((1, "Введено не число"))

        user = db_sess.query(User).get(user_id)
        user.balance += int(amount)
        db_sess.add(Transaction(type=0, product_id=None,
            from_id=None, to_id=user_id, amount=amount))
        db_sess.commit()


    def get_product(self, product_id:int):
        db_sess = self.create_session()
        product = db_sess.query(Product).get(product_id)

        if product is None:
            self.success = False
            self.errors.append((0, "Продукт с этим id не найден."))
            return None

        previous_price = product.price
        discount_price = product.discount_price

        if discount_price is not None:
            discount = round((previous_price - discount_price) / previous_price * 100)
            price = toRub(int(discount_price))
            previous_price = toRub(int(previous_price))

        else:
            price = toRub(int(previous_price))
            previous_price = None
            discount = None

        return {
            "id": product_id,
            "name": product.name,
            "shop_name": product.seller.shop_name,
            "category_id": product.category_id,
            "rating": 4.9,
            "tag_check": True,
            "tag_new": abs((datetime.now() - product.created_date).days) < 15,
            "tag_sale": product.count < 100,
            "description": product.description,
            "price": price,
            "previous_price": previous_price,
            "discount": discount,
            "cover_src": product.img_src.replace("static/", ""),
        }

    def get_latest_products(self, count=10):
        db_sess = self.create_session()
        last_products = db_sess.query(Product).order_by(Product.id.desc()).limit(count).all()
        return [self.get_product(product.id) for product in last_products]


    def get_recommend_products(self, product_id, count=10):
        db_sess = self.create_session()
        product = db_sess.query(Product).get(product_id)
        recommended_products = db_sess.query(Product).order_by(
            Product.id.desc()).filter(Product.category_id ==
            product.category_id, Product.id != product_id).limit(count).all()
        return [self.get_product(prod.id) for prod in recommended_products]


    def get_recommend_products_cart(self, products, count=10):
        db_sess = self.create_session()
        categories_ids = list(map(lambda x: x["category_id"], products))
        products_ids = list(map(lambda x: x["id"], products))
        recommended_products = db_sess.query(Product).order_by(
            Product.id.desc()).filter(Product.category_id.in_(categories_ids),
            ~Product.id.in_(products_ids)).limit(count).all()
        return [self.get_product(prod.id) for prod in recommended_products]