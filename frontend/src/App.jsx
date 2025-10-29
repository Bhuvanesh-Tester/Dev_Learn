import { useState } from "react";
import Login from "./components/Login";
import Register from "./components/Register";

export default function App() {
  const [view, setView] = useState("login");

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>FastAPI + React Auth</h1>
      <div style={{ marginBottom: "20px" }}>
        <button onClick={() => setView("login")}>Login</button>
        <button onClick={() => setView("register")}>Register</button>
      </div>

      {view === "login" ? <Login /> : <Register />}
    </div>
  );
}
