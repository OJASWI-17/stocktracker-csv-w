from celery import shared_task
import pandas as pd
import time
from channels.layers import get_channel_layer
import asyncio
import threading

# Path to CSV file
CSV_FILE_PATH = "C:/projects/stocktracker/stockproject/mainapp/generated_stock_data.csv"

# Load CSV into a DataFrame
df = pd.read_csv(CSV_FILE_PATH)

# Dictionary to track current index for each stock
stock_indices = {ticker: 0 for ticker in df["ticker"].unique()}

# Graceful shutdown flag
stop_flag = threading.Event()

def fetch_stock_data_from_csv(selected_stocks):
    """Fetch stock data from CSV, simulating real-time updates."""
    global stock_indices
    data = {}

    for ticker in selected_stocks:
        stock_data = df[df["ticker"] == ticker]
        index = stock_indices.get(ticker, 0)

        # If we reach the end of the dataset, loop back to the beginning
        if index >= len(stock_data):
            index = 0

        row = stock_data.iloc[index]

        # Convert NumPy types to native Python types
        data[ticker] = {
            "current_price": float(row["current_price"]),
            "previous_close": float(row["previous_close"]),
            "volume": int(row["volume"]),
            "market_cap": float(row["market_cap"]),
            "open_price": float(row["open_price"]),
            "day_high": float(row["day_high"]),
            "day_low": float(row["day_low"]),
        }

        # Move to the next index for the next call
        stock_indices[ticker] = index + 1

    return data

@shared_task
def update_stock(selected_stocks):
    """Celery task to fetch and broadcast stock data every 10 seconds."""
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()  # Create the event loop once
    asyncio.set_event_loop(loop)

    try:
        while not stop_flag.is_set():
            data = fetch_stock_data_from_csv(selected_stocks)
            print("Updated Stock Data:",data)  # Debugging log

            # Send data to WebSockets
            loop.run_until_complete(channel_layer.group_send("stock_track", {
                "type": "send_stock_update",
                "message": data,
            }))

            time.sleep(10)  # Wait for 10 seconds before fetching again
    except KeyboardInterrupt:
        print("Task stopped gracefully.")
    finally:
        loop.close()  # Clean up the event loop  





