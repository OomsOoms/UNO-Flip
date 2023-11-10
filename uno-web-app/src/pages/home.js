import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
  document.title = "UNO | Home"

  return (
    <div>
      <h1>Welcome to UNO Flip!</h1>
      <p>Are you ready to flip the game on its head?</p>
      <Link to="/join-game">Play Now</Link>
    </div>
  );
};

export default Home;
