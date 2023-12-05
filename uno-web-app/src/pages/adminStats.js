import { useState, useEffect } from "react";
import "../scss/adminStats.scss";
import { apiUrl } from "../index.js";

function AdminStats() {
  document.title = "UNO | Admin Stats";

  const [gameStats, setGameStats] = useState([]);
  const [websocketStats, setWebsocketStats] = useState({});

  useEffect(() => {
    const url = apiUrl + "/admin_stats";
    const options = {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    };
    fetch(url, options)
      .then((response) => response.json())
      .then((data) => {
        setGameStats(data.gameStats);
        setWebsocketStats(data.websocketStats);
        console.log(data.gameStats);
        console.log(data.websocketStats);
      })
      .catch((error) => console.log(error));
  }, []);

  return (
    <>
      <h2>Websockets</h2>
      <div className="stats">
        <ul>
          {Object.entries(websocketStats).map(([key, value]) => (
            <WebsocketStatsItem key={key} websocket={value} websocketKey={key} />
          ))}
        </ul>
      </div>
      <h2>Games</h2>
      <div className="stats">
        <ul>
          {gameStats.map((game, index) => (
            <GameStatsItem key={index} game={game} />
          ))}
        </ul>
      </div>
    </>
  );
}

function WebsocketStatsItem({ websocket, websocketKey }) {
  return (
    <li>
      <h2>{websocketKey}</h2>
      <p>Game ID: {websocket.gameId}</p>
      <p>Player ID: {websocket.playerId}</p>
    </li>
  );
}

function GameStatsItem({ game }) {
  return (
    <li>
      <h2>{game.gameId}</h2>
      <p>Players: {JSON.stringify(game.players)}</p>
      <p>Host: {game.host}</p>
      <p>Current Player Id: {game.currentPlayerId}</p>
      <p>Current Player Index: {game.currentPlayerIndex}</p>
      <p>Player scores: {game.playerScores}</p>
      <table>
        <tr>
          <td>Deck Length</td>
          <td>{game.deckLength}</td>
          <td>Discard Pile Length</td>
          <td>{game.discardLength}</td>
        </tr>
        <tr>
          <td>Discard Top</td>
          <td>discardTop</td>
          <td>Game Direction</td>
          <td>{game.gameDirection}</td>
        </tr>
        <tr>
          <td>Game Flip</td>
          <td>{game.gameFlip}</td>
          <td>Game Started</td>
          <td>{game.gameStarted}</td>
        </tr>
      </table>
    </li>
  );
}

export default AdminStats;
