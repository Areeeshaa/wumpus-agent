from flask import Flask, request, jsonify
from flask_cors import CORS
from wumpus import create_world, step_agent, get_state

app = Flask(__name__)
CORS(app)

world = None

@app.route('/init', methods=['POST'])
def init():
    global world
    data = request.json
    rows = data.get("rows", 4)
    cols = data.get("cols", 4)
    world = create_world(rows, cols)
    return jsonify({"message": "World initialized"})

@app.route('/state', methods=['GET'])
def state():
    return jsonify(get_state(world))

@app.route('/step', methods=['POST'])
def step():
    step_agent(world)
    return jsonify(get_state(world))

if __name__ == '__main__':
    app.run(debug=True)