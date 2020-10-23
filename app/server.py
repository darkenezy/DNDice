from flask import Flask, Response, request, redirect, jsonify, render_template
from collections import OrderedDict
import pydash as _
import random

from models import Dice
from utils import ColorFactory, get_auth_code


# Initialize
color_factory = ColorFactory()
app = Flask(__name__, static_url_path="/static")
db = {}


# Api section
@app.route("/api/v1/auth")
def authorize():
    auth_code = get_auth_code(request, allow_create=True)
    response = redirect("/game")
    response.set_cookie("auth_code", auth_code)
    return response


@app.route("/api/v1/get_dice", methods=["GET"])
def get_dice():
    auth_code = get_auth_code(request)
    if not auth_code:
        return redirect("/api/v1/auth", status=401)

    response = list(db.get(auth_code, OrderedDict()).values())
    return jsonify(response), 200


@app.route("/api/v1/add_dice", methods=["POST"])
def add_dice():
    auth_code = get_auth_code(request)
    if not auth_code:
        return redirect("/api/v1/auth")

    dice_id = str(random.randint(100000, 999999))
    dice_desc = request.json["dice_desc"]
    color = color_factory.get_color()

    dice = Dice(dice_id=dice_id, dice_desc=dice_desc, color=color)
    if not dice.is_valid():
        return Response("Invalid dice description", 400)

    db[auth_code] = db.get(auth_code, OrderedDict())
    db[auth_code][dice_id] = dice.to_representation()
    return jsonify(db[auth_code][dice_id]), 201


@app.route("/api/v1/remove_dice/<dice_id>", methods=["DELETE"])
def remove_dice(dice_id):
    auth_code = get_auth_code(request)
    if not auth_code:
        return redirect("/api/v1/auth"), 401

    if dice_id == "all":
        db[auth_code].clear()
        return Response("OK", 204)
    if _.get(db, f"{auth_code}.{dice_id}"):
        del db[auth_code][dice_id]
        return Response("OK", 204)
    return Response("Invalid dice_id", 400)


@app.route("/api/v1/roll", methods=["POST"])
def roll_dice():
    auth_code = get_auth_code(request)
    if not auth_code:
        return redirect("/api/v1/auth")

    db[auth_code] = db.get(auth_code, OrderedDict())
    for dice_id in db[auth_code]:
        representation = db[auth_code][dice_id]
        dice = Dice(**representation)
        dice.roll()
        db[auth_code][dice_id] = dice.to_representation()

    return Response("OK", 200)


@app.route("/game")
def game():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
