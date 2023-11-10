import React from "react";
import { Link } from "react-router-dom";
import "../styles/header.css";

function Header() {
  return (
    <header>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/join-game">Join Game</Link>
          </li>
          <li>
            <Link to="/create-game">Create Game</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;
