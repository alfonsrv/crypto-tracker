from django.shortcuts import render
from django.conf import settings

from crypto.models import Crypto
from crypto.selectors import crypto_invest, crypto_ohlc


def landing(request):
    crypto_queryset = Crypto.objects\
        .order_by('order', 'symbol')\
        .prefetch_related('data', 'purchases')\
        .filter(enabled=True)
    cryptos = crypto_invest(
        crypto_queryset=crypto_queryset
    )

    crypto_charts = []
    if not request.GET.get('charts'):
        # ?charts param to disable chart rendering
        crypto_charts = [
            crypto_ohlc(crypto=crypto) for crypto
            in cryptos.filter(show_chart=True)
        ]

    context = {
        'cryptos': cryptos,
        'crypto_charts': crypto_charts
    }
    return render(request, 'crypto/dashboard.html', context)
