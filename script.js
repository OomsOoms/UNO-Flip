const apiUrl = "http://localhost:8000"

// Function to handle the click event for the "Join!" button
const joinGameButton = document.getElementById("joinGameButton");
const gameIdInput = document.getElementById("gameIdInput");
const usernameInput = document.getElementById("usernameInput");
const createGameButton = document.getElementById("createGameButton");

joinGameButton.addEventListener("click", function() {
    var gameid = gameIdInput.value;
    var usernameinput = usernameInput.value;

    var jsonData = {
        "game_id": gameid,
        "player_name": usernameinput
    };

    var jsonString = JSON.stringify(jsonData);

    var apiEndpointUrl = apiUrl + "/join_game";

    fetch(apiEndpointUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: jsonString
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.detail === "Game is full") {
            console.error("Game is full");
            // Handle the scenario where the game is full
        } else {
            console.log(data);

            document.cookie = "game_id=${respomse.game_id}";
            document.cookie = "player_id=${respomse.player_id}";
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
})

// Function to handle the click event for the "Create game" button
createGameButton.addEventListener("click", function() {
    createGameButton
    var usernameinput = usernameInput.value;

    if (usernameinput.length == 0) {
        console.log("Username is empty");
        usernameInput.style.borderColor = 'red';

        setTimeout(() => {
            usernameInput.style.borderColor = "rgb(70, 70, 70)";
        }, 1000);

        return;
    };

    var jsonData = {
        "player_name": usernameinput
    };

    var jsonString = JSON.stringify(jsonData);

    var apiEndpointUrl = apiUrl + "/create_game";

    fetch(apiEndpointUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: jsonString
    })
    .then(response => {
        return response.json();
      })
    .then(data => {
        document.cookie = `game_id=${data.game_id}`;
        document.cookie = `player_id=${data.player_id}`;
        console.log("Game created " + data.game_id);
        console.log("Player Added: " + usernameinput + " ID: " + data.player_id + " to game " + data.game_id);
        window.location.href = `lobby.html?game_id=${data.game_id}&player_id=${data.player_id}`;
    })
    .catch(error => {
        console.error("There was a problem with the fetch operation:", error);
    });
})

// Function to load the lobby page
function loadLobby() {
    console.log("Loading lobby")
};