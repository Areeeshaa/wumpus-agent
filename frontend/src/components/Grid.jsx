export default function Grid({ grid, agent, move }) {
  return (
    <div className="bg-gray-800 p-4 rounded-2xl shadow-2xl">
      {grid.map((row, i) => (
        <div key={i} className="flex justify-center">
          {row.map((cell, j) => {
            const isAgent = agent.x === i && agent.y === j;

            let color = "bg-gray-600";

            if (isAgent) color = "bg-blue-500";
            else if (cell.revealed && cell.pit) color = "bg-red-600";
            else if (cell.revealed && cell.wumpus) color = "bg-red-800";
            else if (cell.revealed) color = "bg-green-600";

            return (
              <div
                key={j}
                onClick={() => move(i, j)}
                className={`w-14 h-14 m-1 rounded-lg flex items-center justify-center cursor-pointer transition-all duration-200 hover:scale-110 ${color}`}
              >
                {isAgent ? "🤖" : ""}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}