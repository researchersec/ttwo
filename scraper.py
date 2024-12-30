import yfinance as yf
import requests
from bs4 import BeautifulSoup
import json

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
    if news_table:
        for row in news_table.find_all("tr"):
            title_cell = row.find("a")
            date_cell = row.find("td")
            if title_cell and date_cell:
                news_data.append({
                    "date_time": date_cell.text.strip(),
                    "title": title_cell.text,
                })
    with open("data/news_data.json", "w") as f:
        json.dump(news_data, f, indent=4)

if __name__ == "__main__":
    fetch_stock_data()
    fetch_news()
