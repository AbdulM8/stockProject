import requests
from twilio.rest import Client

STOCKS = [
    {"symbol": "TSLA", "company": "Tesla Inc"},
    {"symbol": "AAPL", "company": "Apple Inc"},
    {"symbol": "AMZN", "company": "Amazon.com Inc"}
]

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://www.newsapi.org/v2/everything"

STOCK_API_KEY = "62Y14KEHKM1J0VPH"
NEWS_API_KEY = "a5a0d6bb2a1e4ea392ddb5fd1dbf19f8"

TWILIO_SID = "AC539fc4574d17bb3751ad5dbf5d229187"
TWILIO_AUTH_TOKEN = "9dccc85773880cd00d7a3ed946a51272"

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

for item in STOCKS:
    STOCK = item["symbol"]
    COMPANY_NAME = item["company"]

    STOCK_PARAMS = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": STOCK_API_KEY,
    }

    response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMS)
    response.raise_for_status()
    data = response.json()["Time Series (Daily)"]

    # Convert the daily data into a list of dicts and grab the two most recent days
    data_list = [value for (date, value) in data.items()]
    yesterday_data = data_list[0]
    day_before_yesterday_data = data_list[1]

    yesterday_closing_price = float(yesterday_data["4. close"])
    day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

    difference = yesterday_closing_price - day_before_yesterday_closing_price
    diff_percent = round((difference / day_before_yesterday_closing_price) * 100, 2)

    up_down = "🔺" if difference > 0 else "🔻"

    if abs(diff_percent) > 1:
        news_params = {
            "apiKey": NEWS_API_KEY,
            "qInTitle": COMPANY_NAME,
        }
        news_response = requests.get(NEWS_ENDPOINT, params=news_params)
        news_response.raise_for_status()
        articles = news_response.json()["articles"]

        three_articles = articles[:3]

        formatted_articles = [
            f"{STOCK}: {up_down}{diff_percent}%\n"
            f"Headline: {article['title']}\n"
            f"Brief: {article['description']}"
            for article in three_articles
        ]

        for article in formatted_articles:
            message = client.messages.create(
                body=article,
                from_="+18444405412",
                to="+19294628992"
            )
            print(f"Sent message ID: {message.sid}")


