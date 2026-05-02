export default function Controls({ rows, cols, setRows, setCols, init, step }) {
  return (
    <div className="mb-4">
      <input
        type="number"
        value={rows}
        onChange={(e) => setRows(Number(e.target.value))}
        className="text-black p-1 mr-2"
      />

      <input
        type="number"
        value={cols}
        onChange={(e) => setCols(Number(e.target.value))}
        className="text-black p-1 mr-2"
      />

      <button onClick={init} className="bg-blue-500 px-3 py-1 mr-2">
        Init
      </button>

      <button onClick={step} className="bg-green-500 px-3 py-1">
        Step
      </button>
    </div>
  );
}