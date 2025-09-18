import React, { useState } from "react";

export default function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async () => {
    const res = await fetch("/api/k8s/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, namespace: "default" })
    });
    const data = await res.json();
    setResponse(JSON.stringify(data, null, 2));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>K8s NLP Query</h1>
      <input
        type="text"
        placeholder="Type query e.g., list pods"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: "60%" }}
      />
      <button onClick={handleSubmit}>Submit</button>
      <pre>{response}</pre>
    </div>
  );
}
