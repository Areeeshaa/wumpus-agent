from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

world = {}

# ---------------- CREATE WORLD ----------------
def create_world(n, m):
    grid = [[{
        "pit": False,
        "wumpus": False,
        "revealed": False,
        "breeze": False,
        "stench": False
    } for _ in range(m)] for _ in range(n)]

    # random pits
    for i in range(n):
        for j in range(m):
            if (i, j) != (0, 0) and random.random() < 0.2:
                grid[i][j]["pit"] = True

    # wumpus
    while True:
        wx, wy = random.randint(0, n-1), random.randint(0, m-1)
        if (wx, wy) != (0, 0):
            grid[wx][wy]["wumpus"] = True
            break

    # percepts
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    for i in range(n):
        for j in range(m):
            for dx, dy in dirs:
                ni, nj = i+dx, j+dy
                if 0 <= ni < n and 0 <= nj < m:
                    if grid[ni][nj]["pit"]:
                        grid[i][j]["breeze"] = True
                    if grid[ni][nj]["wumpus"]:
                        grid[i][j]["stench"] = True

    start_cell = grid[0][0]
    start_cell["revealed"] = True
    percepts = []
    if start_cell["breeze"]:
        percepts.append("Breeze")
    if start_cell["stench"]:
        percepts.append("Stench")

    return {
        "grid": grid,
        "agent": {"x": 0, "y": 0},
        "steps": 0,
        "percepts": percepts,
        "gameOver": False
    }

# ---------------- INIT ----------------
@app.route("/init", methods=["POST"])
def init():
    global world
    data = request.json
    world = create_world(data["rows"], data["cols"])
    return jsonify(world)

# ---------------- STATE ----------------
@app.route("/state")
def state():
    return jsonify(world)

# ---------------- MOVE ----------------
@app.route("/move", methods=["POST"])
def move():
    global world
    if world["gameOver"]:
        return jsonify(world)

    data = request.json
    x, y = data["x"], data["y"]

    ax, ay = world["agent"]["x"], world["agent"]["y"]

    # adjacency check
    if abs(ax - x) + abs(ay - y) != 1:
        return jsonify(world)

    world["agent"]["x"], world["agent"]["y"] = x, y
    cell = world["grid"][x][y]

    world["steps"] += 1
    world["percepts"] = []

    # reveal cell
    cell["revealed"] = True

    if cell["breeze"]:
        world["percepts"].append("Breeze")
    if cell["stench"]:
        world["percepts"].append("Stench")

    # GAME OVER conditions
    if cell["pit"] or cell["wumpus"]:
        world["gameOver"] = True

    return jsonify(world)

if __name__ == "__main__":
    app.run(debug=True)