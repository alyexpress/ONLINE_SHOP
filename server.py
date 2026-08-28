from flask import Flask, render_template, redirect, request, abort, jsonify
from flask_login import (LoginManager, login_user, login_required,
                         logout_user, current_user)
from config import *
from app.utils import *
from database import Database


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


@app.context_processor
def inject_config():
    return dict(PROJECT_NAME=PROJECT_NAME, COMPANY_NAME=COMPANY_NAME, CART_COOKIES=CART_COOKIES,
        SHOP_TAB=current_user.is_authenticated and db.has_seller(current_user),
        BALANCE=toRub(current_user.balance) if current_user.is_authenticated else 0)


@login_manager.user_loader
def load_user(user_id):
    return db.load_user(user_id)


@app.route('/login', methods=['GET', 'POST'])
def _login():
    if request.method == 'GET':
        return render_template('system/login.html')

    elif request.method == 'POST':
        # Get input data & check validation
        login = request.form.get('login', "")
        password = request.form.get('password', "")
        user = db.login_user(login, password)

        # Login user if validation success
        if db.success:
            login_user(user, remember=True)
            return redirect("/")

        return render_template('system/login.html', errors=db.errors)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('system/registration.html')

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

        return render_template('system/registration.html', errors=db.errors)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/')
def index():
    products = db.get_latest_products()
    if not db.success: abort(502)
    return render_template('main/index.html', products=products)


@app.route('/product/<int:product_id>')
def _product(product_id):
    product = db.get_product(product_id)
    if not db.success: return abort(404)
    recommended = db.get_recommend_products(product_id)
    return render_template('main/product.html',
        product=product, recommended=recommended)


@app.route('/products')
def _products():
    products = db.get_latest_products()
    if not db.success: abort(502)
    return render_template('main/products.html', products=products)


@app.route('/api/product/<product_id>')
def api_product(product_id):
    if str(request.referrer).startswith(request.host_url):
        product_id = int(product_id.replace(CART_COOKIES, ""))
        return jsonify(db.get_product(product_id))
    return abort(403)



@app.route('/cart')
def cart():
    products = []
    for id, count in get_cart_cookie(request.cookies).items():
        data = db.get_product(id)
        data["cart_count"] = count
        products.append(data)
    products.sort(key=lambda x: x["name"])
    recommended = db.get_recommend_products_cart(products)
    return render_template('main/cart.html',
        products=products, recommended=recommended)


@app.route('/cart/buy')
@login_required
def buy():
    db.purchase(current_user, request.cookies)
    print(db.errors)
    return render_template('main/buy.html')


@app.route('/balance')
@login_required
def balance():
    return render_template('main/balance.html',
        qr_src=qr_generate(current_user.id))


@app.route('/send_money/<int:user_id>', methods=['GET', 'POST'])
def send_money(user_id):
    if request.method == 'GET':
        return render_template('system/send_money.html', sent=False)

    if request.method == 'POST':
        db.replenishment(user_id, request.form.get('money'))
        return render_template('system/send_money.html', sent=True)


@app.route('/shop')
@login_required
def shop():
    seller = db.get_seller(current_user, request.cookies)
    if seller is None: return redirect("/shop/login")
    return render_template('shop/index.html', seller=seller)


@app.route('/shop/login', methods=['GET', 'POST'])
@login_required
def shop_login():
    if request.method == 'GET':
        seller = db.get_seller(current_user, request.cookies)
        if seller is not None: return redirect("/shop")
        if not db.has_seller(current_user): return redirect("/shop/open")
        shop_name = db.get_seller(current_user).shop_name
        return render_template('shop/login.html', shop_name=shop_name)

    elif request.method == 'POST':
        password = request.form.get('password', '')
        seller = db.login_seller(current_user, password)

        if seller is not None:
            response = redirect("/shop")
            response.set_cookie('seller', seller.hashed_password)
            return response

        return render_template('shop/login.html',
            shop_name=db.get_seller(current_user).shop_name)


@app.route('/shop/open', methods=['GET', 'POST'])
@login_required
def shop_open():
    if request.method == 'GET':
        seller = db.get_seller(current_user, request.cookies)
        if seller is not None: return redirect("/shop")
        if db.has_seller(current_user): return redirect("/shop/login")
        return render_template('shop/open.html')

    elif request.method == 'POST':
        # Get input data & check validation
        shop_name = request.form.get('shop_name', '')
        password = request.form.get('password', '')
        seller = db.create_seller(current_user, shop_name, password)

        # Create & login user if validation success
        if db.success:
            response = redirect("/shop")
            response.set_cookie('seller', seller.hashed_password)
            return response

        return render_template('shop/open.html', errors=db.errors)


@app.route('/shop/add', methods=['GET', 'POST'])
@login_required
def shop_add():
    seller = db.get_seller(current_user, request.cookies)
    if seller is None: return redirect("/shop/login")

    if request.method == 'GET':
        return render_template('shop/add.html', seller=seller)
    elif request.method == 'POST':
        # Get input data from form
        name = request.form.get('name', '')
        count = request.form.get('count', '')
        price = request.form.get('price', '')
        description = request.form.get('description', '')
        discount_price = request.form.get('discount_price', '')

        # Get & save cover file
        file = request.files['cover']
        exc = file.filename.split('.')[-1]
        filename = cover_name(exc)
        file.save(filename)
        crop_cover(filename)

        # Add product to database
        db.create_product(seller.id, 0, name, description if description
            else None, filename, int(price), int(count),
            int(discount_price) if discount_price else None)

        if db.success: return redirect("/shop")
        return render_template('shop/add.html', seller=seller, errors=db.errors)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)