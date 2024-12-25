import React, { useState, useEffect } from "react";
import Table from "../components/table";

import { map_player_stats } from "../utils/utils";

const App = () => {

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch data from API
    fetch("http://localhost:5001/api/team/Bronassis")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, []); // Empty dependency array means this runs only once when the component mounts

  console.log(data)
  let cleanedData = []

  if (data !== null) {
    cleanedData = data.roster.map((player) => 
      [player.name, player.team, ...map_player_stats(player.stats)]
    )
  }

  console.log(cleanedData)


  return (
    <div>
      <h1>Hello, World!</h1>
      <Table data={cleanedData} />
    </div>
  );
}

export default App;