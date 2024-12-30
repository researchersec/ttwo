async function fetchData() {
  const stockResponse = await fetch("stock_data.json");
  const newsResponse = await fetch("news_data.json");
  const stockData = await stockResponse.json();
  const newsData = await newsResponse.json();

  const stockList = document.getElementById("stock-list");
  stockList.innerHTML = `
    <li>Open: ${stockData.open}</li>
    <li>High: ${stockData.high}</li>
    <li>Low: ${stockData.low}</li>
    <li>Close: ${stockData.close}</li>
    <li>Volume: ${stockData.volume}</li>
    <li>Weekly Change: ${stockData.weekly_change.toFixed(2)}%</li>
    <li>Monthly Change: ${stockData.monthly_change.toFixed(2)}%</li>
  `;

  const newsList = document.getElementById("news-list");
  newsData.forEach(news => {
    const li = document.createElement("li");
    li.textContent = `${news.date_time} - ${news.title}`;
    newsList.appendChild(li);
  });
}

fetchData();
