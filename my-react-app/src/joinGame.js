import "./joinGame.css"

function UsernameInput() {
  return (
    <input placeholder="Username" id="usernameInput"/>
  );
}

function GameIdInput() {
  return (
    <input placeholder="Game ID" id="gameIdInput"/>
  );
}

function JoinGameButton() {
  return (
    <button id="joinGameButton">Join Game</button>
  );
}

function JoinGame() {
  return (
    <div className="JoinGame">
      <div>
        <h1>Join Game</h1>
      </div>

      <div>
        <UsernameInput />
      </div>

      <div>
        <GameIdInput />
        <JoinGameButton />
      </div>
    </div>
  );
}

export default JoinGame;
