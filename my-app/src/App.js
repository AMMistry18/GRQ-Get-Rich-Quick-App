import './App.css';
import axios from 'axios';
import React, { useEffect, useState } from 'react';

const apiKey = 'PK7LD2WALYEXWWVPOYQL'; // Replace with your API Key ID
const secretKey = 'rQxQlfD4mihWbSxjXJQ3MOXc12e9Xf97iepcCx5w'; // Replace with your Secret Key
const apiServerDomain = 'https://paper-api.alpaca.markets'; // Use the correct domain for paper/live trading

function App() {
  // Create state to store account details
  const [account, setAccount] = useState(null);
  const [error, setError] = useState(null);

  // Fetch account details when component mounts
  useEffect(() => {
    const getAccount = async () => {
      try {
        const response = await axios.get(`${apiServerDomain}/v2/account`, { // Fixed here
          headers: {
            'APCA-API-KEY-ID': apiKey,
            'APCA-API-SECRET-KEY': secretKey
          }
        });
        setAccount(response.data); // Set the fetched account data to state
      } catch (err) {
        setError(err.response ? err.response.data.message : err.message); // Set error message if fetch fails
      }
    };

    getAccount();
  }, []); // Empty dependency array ensures this runs only once

  return (
    <div className="App">
      <h1>Alpaca Account Details</h1>
      {/* Display account details or loading/error messages */}
      {error ? (
        <p style={{ color: 'red' }}>Error: {error}</p>
      ) : account ? (
        <div>
          <p><strong>Account ID:</strong> {account.id}</p>
          <p><strong>Status:</strong> {account.status}</p>
          <p><strong>Buying Power:</strong> ${account.buying_power}</p>
          <p><strong>Cash:</strong> ${account.cash}</p>
          <p><strong>Portfolio Value:</strong> ${account.portfolio_value}</p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;