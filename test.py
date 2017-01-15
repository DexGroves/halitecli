#!/usr/bin/env python


import sys
import os
import halite_cli as hlt


replay = hlt.Replay("hlt/blueonblue.hlt")  # Works on .hlt.gz files too


for i in range(replay.num_frames - 1):
    board = replay.map_at(i)
    render = hlt.render_map(board)
    os.system("clear")
    print(render)
    os.system("sleep 0.05")
