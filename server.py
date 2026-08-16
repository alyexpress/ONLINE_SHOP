from flask import Flask, render_template
from config import *


app = Flask(__name__,
            template_folder=TEMPLATES_DIR,
            static_folder=STATIC_DIR)


@app.context_processor
def inject_config():
    return dict(PROJECT_NAME=PROJECT_NAME,
                COMPANY_NAME=COMPANY_NAME)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
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