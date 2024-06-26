import React, { useState, useEffect } from "react";
import "../scss/gameLobby.scss";
import { apiUrl, webSocketUrl } from "../index.js";

export default function GameRoom() {
  const urlParams = new URLSearchParams(window.location.search);

  const gameId = urlParams.get("id");
  const playerId = sessionStorage.getItem(gameId);

  document.title = "UNO | Lobby " + gameId;

  // When the value changes the component will re-render
  const [lobbyData, setLobbyData] = useState({});

  useEffect(() => {
    const ws = new WebSocket(`${webSocketUrl}/lobby?game_id=${gameId}&player_id=${playerId}`);

    ws.onopen = () => {
      console.log("WebSocket connection opened");
    };
    ws.onclose = (event) => {
      console.log("WebSocket connection disconnected");
      console.log("Reason:", event.reason);
      console.log("Code:", event.code);
      // 1012 is the code for the server shutting down
      if (event.code === 1012) {
        window.location.href = "/";
      }
    };
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // These messages change the state of the component
      if (data.type === "game" || data.type === "lobby" || data.type === "gameOver") {
        data.ws = ws;
        setLobbyData(data);
        // These messages do not change the state of the component
      } else if (data.type === "call_uno") {
        console.log(`${data.playerName} called UNO!`);
      }
    };
    ws.onerror = () => {
      if (document.referrer.includes(window.location.origin)) {
        window.history.back();
      } else {
        window.location.href = "/";
      }
      return;
    };
    return () => {
      console.log("component unmounted");
      ws.close();
    };
  }, [gameId, playerId]);

  switch (lobbyData.type) {
    case "lobby":
      return <Lobby lobbyData={lobbyData} />;
    case "game":
      return <Game lobbyData={lobbyData} />;
    case "gameOver":
      return <GameOver lobbyData={lobbyData} />;
    default:
      return <p>Loading...</p>;
  }
}

function Chat({ lobbyData: { playerName, ws } }) {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const handleMessageChange = (event) => {
    setMessage(event.target.value);
  };

  const handleSendMessage = (event) => {
    event.preventDefault();
    if (message.trim() !== "") {
      ws.send(JSON.stringify({ type: "message", message: `${playerName}: ${message}` }));
      setMessage("");
    }
  };

  useEffect(() => {
    ws.addEventListener("message", function(event) {
      const data = JSON.parse(event.data);
      if (data.type === "message") {
        setMessages((prevMessages) => [...prevMessages, data.message]);
        const messageDisplayBox = document.getElementById("messageDisplayBox");
        messageDisplayBox.scrollTop = messageDisplayBox.scrollHeight;
      }
    });
  }, [ws]);

  return (
    <div>
      <div id="messageDisplayBox">
        {messages.map((message, index) => (
          <p key={index}>{message}</p>
        ))}
      </div>
      <form id="inputContainer">
        <input type="text" value={message} onChange={handleMessageChange} />
        <button onClick={handleSendMessage}>Send</button>
      </form>
    </div>
  );
}

const Lobby = ({ lobbyData, lobbyData: { playerNames, isHost, gameId, playerId, name } }) => {
  const startGame = () => {
    const requestbody = {
      game_id: gameId,
      player_id: playerId,
    };
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestbody),
    };
    fetch(`${apiUrl}/start_game`, requestOptions)
      .then((response) => response.json())
      .then((data) => console.log("Start game button detail:", data.detail));
  };

  return (
    <>
      <Chat lobbyData={lobbyData} />
      <div id="lobbyContainer">
        <h1>Game Lobby<br />{name}</h1>
        <div>
          <p>
            Players: {playerNames.length}/10 | ID {gameId}
          </p>
        </div>
      </div>

      <div id="playerListContainer">
        {playerNames.map((playerName, index) => (
          <p key={index}>{playerName}</p>
        ))}

        {isHost && (
          <button id="startGameButton" onClick={startGame} disabled={playerNames.length < 2} className={playerNames.length < 2 ? "disabled" : ""}>
            Start Game
          </button>
        )}
      </div>
    </>
  );
};

function Game({ lobbyData, lobbyData: { discard, playerHand, isTurn, unoCalled, ws } }) {
  const pickCard = () => {
    ws.send(
      JSON.stringify({
        type: "pick_card",
      })
    );
  };

  const callUno = () => {
    ws.send(
      JSON.stringify({
        type: "call_uno",
      })
    );
  };

  return (
    <div id="gameContainer">
      <Chat lobbyData={lobbyData} />
      <div id="discardContainer">
        <div style={{ backgroundColor: discard.colour }} className="card">
          {discard.action}
        </div>
        <button id="callUnoButton" onClick={callUno} className={`${unoCalled ? "disabled" : ""}`}>
          Call UNO!
        </button>
        <button id="pickCardButton" onClick={pickCard} className={`${isTurn ? "" : "disabled"}`}>
          Pick up card
        </button>
      </div>

      {playerHand.map((card, index) => (
        <Card key={`${card.colour}-${card.action}-${index}`} index={index} card={card} ws={ws} />
      ))}
    </div>
  );
}

function Card({ index, card: { colour, action, isPlayable }, ws, wildColours }) {
  const selectColour = (wildColours) => {
    return new Promise((resolve) => {
      const input = prompt("Enter a value:");
      resolve(input);
    });
  };

  const selectCard = () => {
    if (colour === null) {
      // Run code to get input
      const input = selectColour(wildColours);

      // Send ws json once input is obtained
      input.then((selectedColour) => {
        ws.send(
          JSON.stringify({
            type: "play_card",
            index: index,
            wildColour: selectedColour,
          })
        );
      });
    } else {
      ws.send(
        JSON.stringify({
          type: "play_card",
          index: index,
          wildColour: null,
        })
      );
    }
  };

  return (
    <button style={{ backgroundColor: colour }} className={`card playable ${isPlayable ? "" : "disabled"}`} onClick={selectCard}>
      {action}
    </button>
  );
}

function GameOver({ lobbyData: { score } }) {
  return (
    <div id="gameOverContainer">
      <h1>Game Over</h1>
      <p>Score: {score}</p>
    </div>
  );
}
