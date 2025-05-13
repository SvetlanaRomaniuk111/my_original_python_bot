from operator import ge
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from tomlkit import item
import requests

TOKEN = "7159809064:AAEYheRT49t5DKTYOMVbhDFXUbamMXgQCbk"
CRYPTO_NAME_TO_TICKER = {
    "Bitcoin": "BTCUSDT",
    "Ethereum": "ETHUSDT",
    "Doge": "DOGEUSDT"
}
CRYPTO_TICKER_TO_NAME = {v: k for k, v in CRYPTO_NAME_TO_TICKER.items()}

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=3)
    for crypto_name in CRYPTO_NAME_TO_TICKER.keys():
        item_button = KeyboardButton(crypto_name)
        markup.add(item_button)
    bot.send_message(message.chat.id, "Choose a crypto", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in CRYPTO_NAME_TO_TICKER.keys())
def send_price(message):
    crypto_name = message.text
    print(crypto_name)
    ticker = CRYPTO_NAME_TO_TICKER[crypto_name]
    price = get_price_by_ticker(ticker=ticker)  
    bot.send_message(message.chat.id, f"Price of {crypto_name} to USDT is {price}")

def get_price_by_ticker(*, ticker: str) -> float:
    endpoint = f"https://api.binance.com/api/v3/ticker/price"
    params = {
        "symbol": ticker
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        price = round(float(data['price']), 2)
        return price
    else:
        return "Error fetching price"



bot.infinity_polling()