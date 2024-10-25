import React, { useState } from "react";
import Alpaca from "@alpacahq/alpaca-trade-api";

// Initialize Alpaca client
const alpaca = new Alpaca({
  keyId: "PK7LD2WALYEXWWVPOYQL", // Replace with your API key
  secretKey: "rQxQlfD4mihWbSxjXJQ3MOXc12e9Xf97iepcCx5w", // Replace with your secret key
  paper: true, // Set to false if using live trading
});

const StockFetcher = () => {
  const [symbol, setSymbol] = useState("");
  const [stockData, setStockData] = useState(null);
  const [error, setError] = useState("");

  const fetchStockData = async (symbol) => {
    try {
      // Fetch latest trade data for the stock symbol
      const latestTrade = await alpaca.getLatestTrade(symbol);
      setStockData(latestTrade);
      setError(""); // Clear any previous error
    } catch (err) {
      setStockData(null); // Clear previous data
      setError("Error fetching stock data: " + err.message);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetchStockData(symbol);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          placeholder="Enter stock symbol (e.g., AAPL)"
        />
        <button type="submit">Fetch Stock Data</button>
      </form>
      {error && <p>{error}</p>}
      {stockData && (
        <div>
          <h3>Stock Data for {symbol}</h3>
          <pre>{JSON.stringify(stockData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default StockFetcher;