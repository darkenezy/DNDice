from flask import Flask, Response, request, redirect, jsonify, render_template
from collections import OrderedDict
from random import randint
import pydash as _
import re


class Dice:
    def __init__(self, d):
        self._d = d or ""
        self._value = None
        self._faces = None

    def is_valid(self):
        return re.match(r"[Dd]([1-9][0-9]*)", self._d)

    @property
    def faces(self):
        if self._faces is None:
            match = self.is_valid()
            self._faces = int(match.group(1)) if match else 0
        return self._faces

    def roll(self):
        self._value = randint(1, self.faces)
        return self._value

    def to_representation(self):
        return {"d": self._d, "value": self._value}


# Мне лень сюда постгрес приколачивать
db = {
    "9999": {  # Example entry
        "dice": {
            "123": Dice("D8"),
            "323": Dice("D10")
        },
    }
}


# Flask app
app = Flask(__name__, static_url_path="/static")


# Util
def get_auth_code(request, allow_create=False):
    auth_code = request.cookies.get("auth_code")
    if allow_create and not auth_code:
        auth_code = str(randint(10000, 99999))
    return auth_code


@app.route("/api/v1/auth")
def authorize():
    auth_code = get_auth_code(request, allow_create=True)
    response = redirect("/game")
    response.set_cookie("auth_code", auth_code)
    return response


@app.route("/api/v1/get_dice")
def get_dice():
    auth_code = get_auth_code(request)
    if not auth_code:
        return redirect("/api/v1/auth", status=401)

    db[auth_code] = db.get(auth_code, OrderedDict())
    response = _.map_values(db[auth_code], Dice.to_representation)
    return jsonify(response), 200


@app.route("/api/v1/add_dice", methods=["POST"])
def add_dice():
    auth_code = get_auth_code(request)
    if not auth_code:
        return redirect("/api/v1/auth")

    dice_id, dice_type = _.at(request.json, "dice_id", "dice_type")

    dice = Dice(dice_type)
    if not dice.is_valid():
        return Response("Invalid dice description", 400)

    db[auth_code] = db.get(auth_code, OrderedDict())
    db[auth_code][dice_id] = dice
    return Response("OK", 201)


@app.route("/api/v1/remove_dice", methods=["POST"])
def remove_dice():
    auth_code = get_auth_code(request)
    if not auth_code:
        return redirect("/api/v1/auth", status=401)

    dice_id = request.json.get("dice_id")
    if _.get(db, f"{auth_code}.{dice_id}"):
        del db[auth_code][dice_id]
        return Response("OK", 204)
    return Response("Invalid dice_id", 400)


@app.route("/api/v1/roll", methods=["POST"])
def roll_dice():
    auth_code = get_auth_code(request)
    if not auth_code:
        return redirect("/api/v1/auth", status=401)

    db[auth_code] = db.get(auth_code, OrderedDict())
    for dice in db[auth_code].values():
        dice.roll()

    return Response("OK", 200)


@app.route("/game")
def game():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
