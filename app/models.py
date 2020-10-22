import re
import random


class Dice:
    def __init__(self, desc, value="?", color=None):
        self._desc = desc or ""
        self._value = value
        self._color = color
        self._faces = None

    def is_valid(self):
        return re.match(r"[Dd]([1-9][0-9]*)", self._desc)

    @property
    def faces(self):
        if self._faces is None:
            match = self.is_valid()
            self._faces = int(match.group(1)) if match else 0
        return self._faces

    def roll(self):
        self._value = random.randint(1, self.faces)
        return self._value

    def to_representation(self):
        return {"desc": self._desc, "value": self._value, "color": self._color}