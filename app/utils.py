import hashlib
from config import CART_COOKIES, COVER_DIR
from flask import request
import qrcode, base64, io
from datetime import datetime
from os.path import join
from PIL import Image


def hashed_password(password):
    password = "VaLen3n" + password
    return hashlib.sha256(password.encode()).hexdigest()


def get_cart_cookie(cookies):
    res = {}
    for key, val in cookies.items():
        if key.startswith(CART_COOKIES):
            res[int(key.split("_")[1])] = int(val)
    return res


def toRub(num):
    return ' '.join(str(num)[::-1][i : i + 3] for i in
        range(0, len(str(num)), 3))[::-1] + " ₽"


def qr_generate(user_id:int):
    base_url = request.host_url.rstrip('/')
    url = f"{base_url}/send_money/{user_id}"

    img = qrcode.make(url)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return f"data:image/png;base64,{img_base64}"


def cover_name(exc):
    name = datetime.now().strftime("%Y%m%d%H%M%S")
    return join(COVER_DIR, f"{name}.{exc}")


def crop_cover(filename):
    img = Image.open(filename)
    width, height = img.size

    if width * 3 > height * 2:
        new_height = height
        new_width = int(height * 2 / 3)
    else:
        new_width = width
        new_height = int(width * 3 / 2)

    offset_x = (width - new_width) // 2
    offset_y = (height - new_height) // 2

    box = (offset_x, offset_y, offset_x + new_width, offset_y + new_height)

    cropped_img = img.crop(box)
    cropped_img.save(filename)