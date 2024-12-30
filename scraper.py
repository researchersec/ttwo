import yfinance as yf
import requests
from bs4 import BeautifulSoup
import json
import datetime

def fetch_stock_data():
    ticker = "TTWO"
    stock = yf.Ticker(ticker)
    history = stock.history(period="1mo")
    daily = history.iloc[-1]
    weekly_change = (history['Close'].iloc[-1] - history['Close'].iloc[-5]) / history['Close'].iloc[-5] * 100
    monthly_change = (history['Close'].iloc[-1] - history['Close'].iloc[0]) / history['Close'].iloc[0] * 100
    stock_data = {
        "open": daily['Open'],
        "high": daily['High'],
        "low": daily['Low'],
        "close": daily['Close'],
        "volume": daily['Volume'],
        "weekly_change": weekly_change,
        "monthly_change": monthly_change,
    }
    with open("data/stock_data.json", "w") as f:
        json.dump(stock_data, f, indent=4)

def fetch_news():
    url = "https://finviz.com/quote.ashx?t=TTWO"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    news_table = soup.find("table", class_="fullview-news-outer")
    
    news_data = []
    last_date = None  # To store the last date seen

    if news_table:
        for row in news_table.find_all("tr"):
            title_cell = row.find("a")
            date_cell = row.find("td")
            
            # If both title and date exist
            if title_cell:
                title = title_cell.text.strip()
                
                if date_cell:
                    date_text = date_cell.text.strip()
                    # If there's a date, store it as the last date
                    if date_text != "":  
                        last_date = date_text
                        date_time = date_text
                    else:
                        # If there's no date, use the last seen date
                        date_time = last_date if last_date else "Unknown"
                else:
                    # Fallback in case there's no date cell
                    date_time = last_date if last_date else "Unknown"
                
                # Append the news item with its date and title
                news_data.append({
                    "date_time": date_time,
                    "title": title,
                })

    with open("data/news_data.json", "w") as f:
        json.dump(news_data, f, indent=4)

if __name__ == "__main__":
    fetch_stock_data()
    fetch_news()
