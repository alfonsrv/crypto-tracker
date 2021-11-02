from django import template
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma

from forex_python.converter import CurrencyCodes

register = template.Library()

@register.filter
def currency_symbol(value):
    if not value: return '–'
    c = CurrencyCodes()
    currency = settings.TARGET_CURRENCY or settings.COINMARKET_CURRENCY
    symbol = c.get_symbol(currency)
    crypto_value = float(cryptoformat(value))
    comma_value = intcomma(crypto_value)
    if len(str(crypto_value)) > len(comma_value):
        comma_value = f'{comma_value}0'

    return f'{comma_value} {symbol}'


@register.filter
def percent(value):
    if not value: return '–'
    value = float(value)
    return f'{value:+.2f} %'


@register.filter
def cryptoformat(value):
    """ Only gets the next 3 decimals after the first non-zero value
    after the decimal point while ensuring floats are returned with "." """
    float_format = 2
    if value < 1:
        # finds first number after zeroes
        float_format = int(str(value).partition('.')[2]) + 100

    value = round(value, float_format)
    return f'{value:f}'
