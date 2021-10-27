from datetime import datetime
import logging

from django.conf import settings
import requests
from forex_python.converter import CurrencyRates, RatesNotAvailableError

from crypto.constants import ENDPOINT, HEADERS
from crypto.models import Crypto, CryptoData, Alert

logger = logging.getLogger(__name__)

def percentual_change(*, crypto_ticker: str):
    pass


def crypto_update():
    """ Updates all enabled Cryptos' price information """
    cryptos = Crypto.objects.filter(enabled=True).values_list('symbol', flat=True)
    if not cryptos:
        logger.info('No cryptos available for updating; skipping...')
        return
    crypto_quotes = crypto_get(crypto_symbols=cryptos)
    for symbol, quote in crypto_quotes.items():
        CryptoData.objects.create(
            crypto=Crypto.objects.get(symbol=symbol),
            source_price=quote.get('price'),
            source_currency=quote.get('currency'),
            percent_day=quote.get('percent_day'),
            rank=quote.get('rank'),
        )
    logger.info('Updated all crypto price information')


def crypto_get(*, crypto_symbols: list) -> dict:
    """ Queries the latest cryptos price information from CoinMarket """
    HEADERS.setdefault('X-CMC_PRO_API_KEY', settings.COINMARKET_KEY)
    params = {
        'symbol': ','.join(crypto_symbols),
        'convert': settings.COINMARKET_CURRENCY
    }
    response = requests.get(
        f'{ENDPOINT}/v1/cryptocurrency/quotes/latest',
        headers=HEADERS,
        params=params
    )
    data = response.json()
    if data.get('error_code'):
        logger.warning(f'CoinMarket returned an error! Response: {data}')
    logger.info(f'Consumed {data.get("status").get("credit_count")} CoinMarket Credit for request')

    for symbol in crypto_symbols:
        coin_data = data.get('data').get(symbol)
        coin_quote = coin_data.get('quote').get(settings.COINMARKET_CURRENCY)
        logger.debug(
            f'[{symbol}] {coin_quote.get("price")} € '
            f'({coin_quote.get("percent_change_24h"):+.2f} %) -- '
            f'Rank: {coin_data.get("cmc_rank")}'
        )

    return {
        symbol: {
            'rank': value.get('cmc_rank'),
            'price': value.get('quote').get(settings.COINMARKET_CURRENCY).get('price'),
            'percent_day': value.get('quote').get(settings.COINMARKET_CURRENCY).get('percent_change_24h'),
            'currency': settings.COINMARKET_CURRENCY
        } for (symbol, value) in data.get('data').items()
    }


def currency_convert(*, source_currency: str, target_currency: str, source_amount: float, timestamp: datetime = None) -> float:
    """ Converts currencies using forex-python. An optional timestamp can be specified for
    historic exchange rates. If the historic exchange rate lookup fails, the current
    exchange rate is used instead """
    c = CurrencyRates()
    try:
        return c.convert(
            source_currency,
            target_currency,
            source_amount,
            date_obj=timestamp
        )
    except RatesNotAvailableError:
        return c.convert(
            source_currency,
            target_currency,
            source_amount
        )


def alert_price(*, alert: Alert) -> None:
    crypto_percent = alert.crypto.data.latest().percent_day

    url = f'https://api.pushover.net/1/messages.json'
    data = {
        'token': settings.PUSHOVER_APP_TOKEN,
        'user': settings.PUSHOVER_USER_KEY,
        'title': 'Crypto Tracker',
        'sound': 'habbo_cash',
        'message': f'{alert.crypto} surpassed {alert.price} ({crypto_percent:+.2f}%)'
    }

    _ = requests.post(url, data=data)
