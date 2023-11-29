import { useState, useEffect } from "react";
import "../scss/adminStats.scss";
import { apiUrl } from "../index.js";

function AdminStats() {
    document.title = "UNO | Admin Stats"

    const [gameStats, setGameStats] = useState({});
    const [websocketStats, setWebsocketStats] = useState({});

    useEffect(() => {
        const url = apiUrl + "/admin_stats";
        const options = {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        };
        fetch(url, options)
            .then(response => response.json())
            .then(data => {
                setGameStats(data.gameStats);
                setWebsocketStats(data.websocketStats);
                console.log(data.gameStats);
                console.log(data.websocketStats);
            })
            .catch(error => console.log(error));
    }, []);

    return (
        <>
            <h1>Game Stats:</h1>
            <pre>{JSON.stringify(gameStats)}</pre>

            <h1>Websocket Stats:</h1>
            <pre>{JSON.stringify(websocketStats)}</pre>
        </>
    )
}

export default AdminStats;
