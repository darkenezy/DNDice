from flask import Flask, Response, request, redirect, jsonify, render_template
from collections import OrderedDict
from bson import ObjectId
import pydash as _

from models import Dice
from pymongo import MongoClient
from utils import ColorFactory, auth_required


# Initialize
color_factory = ColorFactory()
app = Flask(__name__, static_url_path="/static")
db = MongoClient("mongo:27017").dices


# Api section
@auth_required(allow_create=True)
@app.route("/api/v1/auth")
def authorize(auth_code):
    response = redirect("/game")
    response.set_cookie("auth_code", auth_code)
    return response


@app.route("/api/v1/get_dice", methods=["GET"])
@auth_required()
def get_dice(auth_code):
    response = list(db[auth_code].find({}, sort=[("_id", 1)]))
    for dice in response:
        dice["_id"] = str(dice["_id"])
    return jsonify(response), 200


@app.route("/api/v1/add_dice", methods=["POST"])
@auth_required()
def add_dice(auth_code):
    dice_desc = request.json["dice_desc"]
    color = color_factory.get_color()

    dice = Dice(dice_desc=dice_desc, color=color)
    if not dice.is_valid():
        return Response("Invalid dice description", 400)

    dice_id = db[auth_code].insert_one(dice.to_representation()).inserted_id
    document = _.map_values(db[auth_code].find_one(dice_id), str)
    return jsonify(document), 201


@app.route("/api/v1/remove_dice/<dice_id>", methods=["DELETE"])
@auth_required()
def remove_dice(auth_code, dice_id):
    if dice_id == "all":
        db.drop_collection(auth_code)
        return Response("OK", 204)
    document = db[auth_code].find_one(ObjectId(dice_id))
    if document:
        db[auth_code].delete_one(ObjectId(dice_id))
        return Response("OK", 204)
    return Response("Invalid dice_id", 400)


@app.route("/api/v1/roll", methods=["POST"])
@auth_required()
def roll_dice(auth_code):
    response = list(db[auth_code].find({}, sort=[("_id", 1)]))
    for dice in response:
        dice["value"] = Dice(**dice).roll()
        db[auth_code].replace_one({"_id": ObjectId(dice["_id"])}, dice)
    for dice in response:
        dice["_id"] = str(dice["_id"])
    return jsonify(response), 200


@app.route("/game")
@auth_required()
def game(auth_code):
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
