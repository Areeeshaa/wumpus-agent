import { useEffect, useState } from "react";
import Grid from "./components/Grid";

const API = "https://wumpus-agent-production.up.railway.app/";

export default function App() {
  const [grid, setGrid] = useState([]);
  const [agent, setAgent] = useState({ x: 0, y: 0 });
  const [percepts, setPercepts] = useState([]);
  const [steps, setSteps] = useState(0);
  const [gameOver, setGameOver] = useState(false);

  const init = async () => {
    const res = await fetch(API + "/init", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rows: 5, cols: 5 }),
    });

    const data = await res.json();
    updateState(data);
  };

  const updateState = (data) => {
    setGrid(data.grid);
    setAgent(data.agent);
    setSteps(data.steps);
    setPercepts(data.percepts);
    setGameOver(data.gameOver);
  };

  const move = async (x, y) => {
    if (gameOver) return;

    const res = await fetch(API + "/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ x, y }),
    });

    const data = await res.json();
    updateState(data);
  };

  const restartGame = async () => {
    setGameOver(false);
    await init();
  };

  useEffect(() => {
    init();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white flex flex-col items-center justify-center p-6">

      {/* HEADER */}
      <h1 className="text-3xl font-bold mb-4">
        🧠 Wumpus Logic Agent
      </h1>

      {/* DASHBOARD */}
      <div className="flex gap-4 mb-6">
        <div className="bg-gray-800 px-4 py-2 rounded-lg">
          Steps: {steps}
        </div>
        <div className="bg-gray-800 px-4 py-2 rounded-lg">
          Percepts: {percepts.join(", ") || "None"}
        </div>
      </div>

      {/* GRID CENTERED */}
      <div className="flex justify-center items-center">
        <Grid grid={grid} agent={agent} move={move} />
      </div>

      {/* GAME OVER MODAL */}
      {gameOver && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center">
          <div className="bg-gray-900 p-6 rounded-xl shadow-xl text-center">
            <h2 className="text-2xl font-bold text-red-500 mb-3">
              💀 Game Over
            </h2>

            <p className="mb-4 text-gray-300">
              You stepped into danger!
            </p>

            <button
              onClick={restartGame}
              className="bg-green-500 px-4 py-2 rounded-lg hover:bg-green-600"
            >
              Restart Game
            </button>
          </div>
        </div>
      )}

    </div>
  );
}