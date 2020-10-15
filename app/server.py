from flask import Flask, request, jsonify
from random import randint
import re


class Dice:
    def __init__(self, d):
        self.d = d

    @property
    def is_valid(self):
        return re.match(r"[Dd]([1-9][0-9]*)", self.d)

    @property
    def faces(self):
        match = self.is_valid
        if not match:
            return 0
        return int(match.group(1))

    @property
    def value(self):
        return randint(1, self.faces)


app = Flask(__name__)


@app.route('/dice')
def throw_dice():
    response = []
    for d, count in request.args.items():
        dice = Dice(d)
        count = int(count)
        if not dice.is_valid:
            return jsonify({'error': f'{d} is not ad valid dice'}), 400
        response.append([dice.value for i in range(count)])
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0")
