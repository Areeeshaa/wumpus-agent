import random
from logic import update_kb, is_safe

def create_world(rows, cols):
    grid = []

    for i in range(rows):
        row = []
        for j in range(cols):
            row.append({
                "pit": False,
                "wumpus": False,
                "safe": False,
                "visited": False,
                "breeze": False,
                "stench": False
            })
        grid.append(row)

    # place pits
    for i in range(rows):
        for j in range(cols):
            if random.random() < 0.2 and not (i == 0 and j == 0):
                grid[i][j]["pit"] = True

    # place wumpus
    while True:
        x = random.randint(0, rows - 1)
        y = random.randint(0, cols - 1)
        if not (x == 0 and y == 0):
            grid[x][y]["wumpus"] = True
            break

    add_percepts(grid)

    start_cell = grid[0][0]
    start_cell["visited"] = True
    start_cell["safe"] = not (start_cell["pit"] or start_cell["wumpus"])
    percepts = []
    if start_cell["breeze"]:
        percepts.append("Breeze")
    if start_cell["stench"]:
        percepts.append("Stench")

    return {
        "grid": grid,
        "rows": rows,
        "cols": cols,
        "agent": {"x": 0, "y": 0},
        "KB": [{"x": 0, "y": 0, "percepts": percepts}],
        "steps": 0,
        "percepts": percepts
    }

def add_percepts(grid):
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            for dx, dy in dirs:
                nx, ny = i + dx, j + dy
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                    if grid[nx][ny]["pit"]:
                        grid[i][j]["breeze"] = True
                    if grid[nx][ny]["wumpus"]:
                        grid[i][j]["stench"] = True

def get_state(world):
    return {
        "grid": world["grid"],
        "agent": world["agent"],
        "steps": world["steps"],
        "percepts": world["percepts"],
        "gameOver": world.get("gameOver", False)
    }

def move_agent(world, x, y):
    if world.get("gameOver"):
        return False, "Game is over"

    if not isinstance(x, int) or not isinstance(y, int):
        return False, "Coordinates must be integers"

    cx = world["agent"]["x"]
    cy = world["agent"]["y"]
    if abs(cx - x) + abs(cy - y) != 1:
        return False, "Move must be to an adjacent cell"

    if x < 0 or x >= world["rows"] or y < 0 or y >= world["cols"]:
        return False, "Coordinates out of bounds"

    world["agent"] = {"x": x, "y": y}
    world["steps"] += 1

    cell = world["grid"][x][y]
    cell["visited"] = True
    cell["safe"] = not (cell["pit"] or cell["wumpus"])

    if cell["pit"] or cell["wumpus"]:
        world["percepts"] = []
        world["gameOver"] = True
        return True, None

    percepts = []
    if cell["breeze"]:
        percepts.append("Breeze")
    if cell["stench"]:
        percepts.append("Stench")

    world["percepts"] = percepts
    update_kb(world, x, y, percepts)
    return True, None

def step_agent(world):
    x = world["agent"]["x"]
    y = world["agent"]["y"]

    cell = world["grid"][x][y]
    cell["visited"] = True
    cell["safe"] = True

    percepts = []
    if cell["breeze"]:
        percepts.append("Breeze")
    if cell["stench"]:
        percepts.append("Stench")

    world["percepts"] = percepts

    update_kb(world, x, y, percepts)

    moves = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]

    for nx, ny in moves:
        if 0 <= nx < world["rows"] and 0 <= ny < world["cols"]:
            if not world["grid"][nx][ny]["visited"]:
                if is_safe(world, nx, ny):
                    world["agent"] = {"x": nx, "y": ny}
                    world["steps"] += 1
                    return