from flask import Flask, render_template, redirect, request, make_response
from flask_login import (LoginManager, login_user, login_required,
                         logout_user, current_user)
from config import *

from database import Database

from app.utils import get_cart_cookie

from collections import defaultdict

app = Flask(__name__,
            template_folder=TEMPLATES_DIR,
            static_folder=STATIC_DIR)

# Setting secret key from config
app.config['SECRET_KEY'] = SECRET_KEY

# Database init
db = Database(DATABASE_PATH)

# Login manager init
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.load_user(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.context_processor
def inject_config():
    return dict(PROJECT_NAME=PROJECT_NAME,
                COMPANY_NAME=COMPANY_NAME)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def _login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        # Get input data & check validation
        login = request.form.get('login', "")
        password = request.form.get('password', "")
        user = db.login_user(login, password)

        # Login user if validation success
        if db.success:
            login_user(user, remember=True)
            return redirect("/")

        return render_template('login.html', errors=db.errors)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')

    if request.method == 'POST':
        # Get input data & check validation
        username = request.form.get('username', "")
        email = request.form.get('email', "")
        password = request.form.get('password', "")
        new_user = db.create_user(username, email, password)

        # Create & login user if validation success
        if db.success:
            login_user(new_user, remember=True)
            return redirect("/")

        return render_template('registration.html', errors=db.errors)


@app.route('/products')
def products():
    return render_template('products.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/cart/buy')
def cart_buy():
    db.purchase(current_user, get_cart_cookie(request.cookies))
    return render_template('cart_buy.html')

@app.route('/add_product/<int:product_id>')
def add_product(product_id):
    response = redirect("/")
    response.set_cookie(f"{CART_COOKIES}_{product_id}", "1", EXPIRES_COOKIES)
    return response

@app.route('/money')
def money():
    return render_template('money.html')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)