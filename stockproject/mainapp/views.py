from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .tasks import update_stock

# Path to CSV file
CSV_FILE_PATH = "C:/projects/stocktracker/stockproject/mainapp/generated_stock_data.csv"

# Load CSV into a DataFrame
df = pd.read_csv(CSV_FILE_PATH)

# Dictionary to store current index for each stock
stock_indices = {ticker: 0 for ticker in df["ticker"].unique()}

def get_stock_updates(selected_stocks):
    """Fetch stock data from CSV and simulate real-time updates."""
    global stock_indices
    data = {}

    for ticker in selected_stocks:
        stock_data = df[df["ticker"] == ticker]
        index = stock_indices.get(ticker, 0)

        # If we reach the end of the dataset, loop back to the beginning
        if index >= len(stock_data):
            index = 0

        row = stock_data.iloc[index]

        data[ticker] = {
            "current_price": row["current_price"],
            "previous_close": row["previous_close"],
            "volume": row["volume"],
            "market_cap": row["market_cap"],
            "open_price": row["open_price"],
            "day_high": row["day_high"],
            "day_low": row["day_low"],
        }

        # Move to the next index for the next call
        stock_indices[ticker] = index + 1

    return data

def stockPicker(request):
    """View to display available stocks for selection."""
    stock_picker = df["ticker"].unique().tolist()
    return render(request, "mainapp/stockpicker.html", {"stock_picker": stock_picker})

def stockTracker(request):
    """View to fetch initial stock data and trigger Celery updates."""
    selected_stocks = request.GET.getlist("stock_picker")

    if not selected_stocks:
        return JsonResponse({"error": "No stocks selected"}, status=400)

    # Fetch initial stock data to send to frontend
    initial_data = get_stock_updates(selected_stocks)

    # Start Celery task for periodic updates
    update_stock.delay(selected_stocks)

    return render(request, "mainapp/stocktracker.html", {"room_name": "track", "data": initial_data})





















# from django.shortcuts import render
# from django.http import JsonResponse
# import pandas as pd
# import time
# import threading

# # Path to the CSV file
# CSV_FILE_PATH = "C:/projects/stocktracker/stockproject/mainapp/generated_stock_data.csv"

# # Load CSV into a DataFrame
# df = pd.read_csv(CSV_FILE_PATH)

# # Dictionary to store the current index for each stock
# stock_indices = {ticker: 0 for ticker in df["ticker"].unique()}

# def fetch_stock_data_from_csv(selected_stocks):
#     """
#     Fetch stock data from the CSV file, simulating real-time updates.
#     """
#     global stock_indices
#     data = {}

#     for ticker in selected_stocks:
#         stock_data = df[df["ticker"] == ticker]
#         index = stock_indices.get(ticker, 0)

#         # If we reach the end of the dataset, loop back to the beginning
#         if index >= len(stock_data):
#             index = 0

#         row = stock_data.iloc[index]

#         data[ticker] = {
#             "current_price": row["current_price"],
#             "previous_close": row["previous_close"],
#             "volume": row["volume"],
#             "market_cap": row["market_cap"],
#             "open_price": row["open_price"],
#             "day_high": row["day_high"],
#             "day_low": row["day_low"],
#         }

#         # Move to the next index for the next call
#         stock_indices[ticker] = index + 1

#     return data

# def stockPicker(request):
#     """
#     View to display available stocks for selection.
#     """
#     stock_picker = df["ticker"].unique().tolist()
#     return render(request, "mainapp/stockpicker.html", {"stock_picker": stock_picker})

# def stockTracker(request):
#     """
#     View to display stock tracker page with initial data.
#     """
#     selected_stocks = request.GET.getlist("stock_picker")
    
#     if not selected_stocks:
#         return JsonResponse({"error": "No stocks selected"}, status=400)

#     # Fetch initial data for selected stocks
#     data = fetch_stock_data_from_csv(selected_stocks)
#     print(data)

#     return render(request, "mainapp/stocktracker.html", {
#         "data": data,
#         "selected_stocks": selected_stocks,
#         "room_name": "track"
#     })

# def get_stock_updates(request):
#     """
#     API endpoint to fetch updated stock data every 10 seconds.
#     """
#     selected_stocks = request.GET.getlist("stock_picker")
    
#     if not selected_stocks:
#         return JsonResponse({"error": "No stocks selected"}, status=400)

#     data = fetch_stock_data_from_csv(selected_stocks)
#     print(data)
#     return JsonResponse({"data": data})











