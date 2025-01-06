import requests
import click

@click.command()
@click.option("--coin_id", default="bitcoin")
@click.option("--currency", default="eur")
def get_coin_price(coin_id, currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"
    data  = requests.get(url).json()
    coin_price = data[coin_id][currency]
    print(f"The price of {coin_id} is {coin_price:.2f} {currency.upper()}")

if __name__ == "__main__":
    get_coin_price()

"""
(venv) λ py main.py
The price of bitcoin is 95450.00 EUR

(venv) λ py main.py --coin_id=ethereum --currency=usd
The price of ethereum is 3624.81 USD
"""
