import React, { useState } from "react";
import "./App.css";
import Login from "./components/Login";
import FaceRecognition from "./components/FaceRecognition";

function App() {
  const [direct, setDirect] = useState(0);

  return (
    <>
      <div className="App">
        {direct === 0 ? <Login setDirect={setDirect} direct={direct} /> : ""}
        {direct === 1 ? <FaceRecognition setDirect={setDirect} /> : ""}
      </div>
    </>
  );
}

export default App;
