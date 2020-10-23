from flask import request, redirect
from functools import wraps
import seaborn as sns
import random


class ColorFactory:
    def __init__(self):
        self.palette = sns.color_palette("hls", 128)

    @staticmethod
    def _transform_to_hex(color):
        return "#" + "".join(list(map(lambda x: f"{hex(int(255*x))[2:]:0>2}", color)))

    def get_color(self, hexed=True):
        color = random.choice(self.palette)
        return self._transform_to_hex(color) if hexed else color


def get_auth_code(request, allow_create=False):
    auth_code = request.cookies.get("auth_code")
    if allow_create and not auth_code:
        auth_code = str(random.randint(10000, 99999))
    return auth_code


def auth_required(allow_create=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_code = get_auth_code(request, allow_create)
            if not auth_code:
                return redirect("/api/v1/auth", status=401)
            return func(auth_code, *args, **kwargs)
        return wrapper
    return decorator


