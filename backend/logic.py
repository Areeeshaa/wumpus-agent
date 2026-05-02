def update_kb(world, x, y, percepts):
    world["KB"].append({
        "x": x,
        "y": y,
        "percepts": percepts
    })

def is_safe(world, x, y):
    for fact in world["KB"]:
        fx, fy = fact["x"], fact["y"]

        if abs(fx - x) + abs(fy - y) == 1:
            if "Breeze" in fact["percepts"]:
                return False
            if "Stench" in fact["percepts"]:
                return False

    return True