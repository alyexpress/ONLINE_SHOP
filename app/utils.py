import hashlib
from flask import url_for, request
import qrcode
from io import BytesIO
import base64
from config import CART_COOKIES

def hashed_password(password):
    password = "VaLen3n" + password
    return hashlib.sha256(password.encode()).hexdigest()


def get_cart_cookie(cookies):
    res = {}
    for key, val in cookies.items():
        if key.startswith(CART_COOKIES):
            res[int(key.split("_")[1])] = int(val)
    return res


def qr_generate(user_id:int):
    # Build payment URL
    base_url = request.host_url.rstrip('/')
    url = f"{base_url}/get_money/{user_id}"

    # Create QR code
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    # Generate image and encode as base64
    img = qr.make_image(fill_color="black",
                        back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{img_base64}"