import numpy as np
import gzip
import json


class Replay(object):

    def __init__(self, filename=None, width=None, height=None):
        """
        Loads a replay file from disk, or creates a new replay.

        Replay files may be gzip encoded (with a .gz filename).
        Because that's awesome. Keep your replays in gzip kids.
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
              "move": move, "width": self.width, "height": self.height,
              "num_frames": self.num_frames - 1}
        return gm
