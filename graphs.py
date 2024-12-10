import dash
from dash import dcc, html, Input, Output
import pandas as pd
from alpaca.data import StockHistoricalDataClient, StockBarsRequest, TimeFrame
from datetime import datetime, timedelta
import plotly.express as px

# Initialize Alpaca Data Client
data_client = StockHistoricalDataClient("PKQZS7U1Q3KXNXE3UCW7", "c710UmDtzZZUvUBs7L9HNzZXAXh1RXEOWvxNV4NP")


# Define a function to fetch stock data
def fetch_stock_data(symbol, range_type):
    end_date = datetime.now()
    if range_type == "1D":
        start_date = end_date - timedelta(days=1)
        timeframe = TimeFrame.Minute
    elif range_type == "1W":
        start_date = end_date - timedelta(weeks=1)
        timeframe = TimeFrame.Hour
    elif range_type == "1M":
        start_date = end_date - timedelta(days=30)
        timeframe = TimeFrame.Hour
    elif range_type == "3M":
        start_date = end_date - timedelta(days=90)
        timeframe = TimeFrame.Day
    elif range_type == "6M":
        start_date = end_date - timedelta(days=180)
        timeframe = TimeFrame.Day
    elif range_type == "YTD":
        start_date = datetime(end_date.year, 1, 1)
        timeframe = TimeFrame.Day
    elif range_type == "1Y":
        start_date = end_date - timedelta(days=365)
        timeframe = TimeFrame.Day
    elif range_type == "2Y":
        start_date = end_date - timedelta(days=730)
        timeframe = TimeFrame.Week
    elif range_type == "5Y":
        start_date = end_date - timedelta(days=1825)
        timeframe = TimeFrame.Week
    elif range_type == "ALL":
        start_date = datetime(2000, 1, 1)
        timeframe = TimeFrame.Month
    else:
        raise ValueError("Unsupported range type.")

    request_params = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=timeframe,
        start=start_date,
        end=end_date
    )
    bars = data_client.get_stock_bars(request_params)

    # Convert to DataFrame
    data = bars.data[symbol]
    df = pd.DataFrame([{
        "time": bar.timestamp,
        "open": bar.open,
        "high": bar.high,
        "low": bar.low,
        "close": bar.close,
        "volume": bar.volume
    } for bar in data])
    df.set_index("time", inplace=True)
    return df


# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Stock Price Viewer", style={"textAlign": "center"}),

    # Dropdown for selecting the time range
    dcc.Dropdown(
        id="timeframe-dropdown",
        options=[
            {"label": "1 Day", "value": "1D"},
            {"label": "1 Week", "value": "1W"},
            {"label": "1 Month", "value": "1M"},
            {"label": "3 Months", "value": "3M"},
            {"label": "6 Months", "value": "6M"},
            {"label": "Year-to-Date", "value": "YTD"},
            {"label": "1 Year", "value": "1Y"},
            {"label": "2 Years", "value": "2Y"},
            {"label": "5 Years", "value": "5Y"},
            {"label": "All Time", "value": "ALL"}
        ],
        value="1M",  # Default value
        style={"width": "50%", "margin": "0 auto"}
    ),

    # Graph for displaying the stock data
    dcc.Graph(id="stock-graph", style={"height": "600px"})
])


# Callback to update the graph based on the selected time range
@app.callback(
    Output("stock-graph", "figure"),
    [Input("timeframe-dropdown", "value")]
)
def update_graph(selected_timeframe):
    symbol = "AAPL"  # You can make this dynamic as well
    df = fetch_stock_data(symbol, selected_timeframe)

    # Create the Plotly figure
    fig = px.line(
        df,
        x=df.index,
        y="close",
        title=f"{symbol} Stock Prices ({selected_timeframe})",
        labels={"close": "Price", "time": "Time"}
    )
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Price",
        template="plotly_dark"
    )
    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
