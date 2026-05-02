export default function Dashboard({ steps, percepts }) {
  return (
    <div className="mb-4">
      <p>Steps: {steps}</p>
      <p>Percepts: {percepts.join(", ")}</p>
    </div>
  );
}