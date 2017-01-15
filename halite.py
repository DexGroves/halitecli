import pandas as pd
import numpy as np
import math
import gzip
import json


class GameMap(pd.DataFrame):
    _metadata = ['width', 'height']

    def _constructor(self):
        return GameMap


class Replay(object):

    def __init__(self, filename=None, width=None, height=None):
        """
        Loads a replay file from disk, or creates a new replay.

        Replay files may be gzip encoded (with a .gz filename). Because that's awesome. Keep your replays in gzip kids.
        """

        if ".gz" in filename:
            with gzip.open(filename, 'rb') as f:
                data = json.load(f)
        else:
            with open(filename) as f:
                data = json.load(f)

        self.data = data
        self.width = data["width"]
        self.height = data["height"]
        self.num_players = data["num_players"]
        self.num_frames = data["num_frames"]
        self.player_names = data["player_names"]

    def map_at(self, turn, include_moves=False):
        """
        Returns a game map for a given turn.
        """
        production = np.array(self.data['productions'])
        frame = np.array(self.data['frames'][turn])
        strength = frame[:, :, 1]
        owner = frame[:, :, 0]
        move = np.array(self.data['moves'][turn]).flatten()
        gm = {"production": production, "strength": strength, "owner": owner,
              "move": move, "width": self.width, "height": self.height}
        return gm


def render_map(board):
    strength = board["strength"]
    owner = board["owner"]
    production = board["production"]

    data = np.stack([production, strength, owner], axis=2).astype(int)
    colored = np.apply_along_axis(to_clrfrac, 2, data)

    return '\n'.join(np.apply_along_axis(' '.join, 1, colored))


COLORS = [u'\033[39m', u'\033[31m', u'\033[32m', u'\033[33m',
          u'\033[34m', u'\033[35m', u'\033[36m']


def to_clrfrac(element):
    color = COLORS[element[2]]
    numerator = justify_int(element[1], 3, 'right')
    denominator = justify_int(element[2], 2, 'left')
    return color + numerator + '/' + denominator


def justify_int(element, to, how='left'):
    s = str(element)
    if how == 'left':
        return s + ' ' * (to - len(s))
    if how == 'right':
        return ' ' * (to - len(s)) + s
