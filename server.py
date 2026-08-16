from flask import Flask, render_template, redirect, request, flash
from flask_login import (LoginManager, login_user, login_required,
                         logout_user, current_user)
from config import *

from database import Database


app = Flask(__name__,
            template_folder=TEMPLATES_DIR,
            static_folder=STATIC_DIR)
app.config['SECRET_KEY'] = SECRET_KEY

db = Database(DATABASE_PATH)
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
def login():
    if request.method == 'POST':
        login = request.form.get('login', "")
        password = request.form.get('password', "")
        user = db.login_user(login, password)
        if not db.success:
            return render_template('login.html')
        login_user(user, remember=True)
        return redirect("/")
    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('username', "")
        email = request.form.get('email', "")
        password = request.form.get('password', "")
        new_user = db.create_user(username, email, password)
        if not db.success:
            return render_template('registration.html')
        login_user(new_user, remember=True)
        return redirect("/")
    return render_template('registration.html')


@app.route('/products')
def products():
    return render_template('products.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/money')
def money():
    return render_template('money.html')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)