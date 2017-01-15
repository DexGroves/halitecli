import halite as hlt

replay = hlt.Replay("hlt/1482196058-1239.hlt")  # Works on .hlt.gz files too
board = replay.map_at(0)
hlt.render_map(board)
