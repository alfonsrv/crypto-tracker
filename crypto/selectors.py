from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import QuerySet, Sum, F, OuterRef, Subquery, Func, Max, Min

from crypto.models import CryptoData, Crypto


def crypto_invest(*, crypto_queryset: QuerySet) -> QuerySet:
    """ Adds overall information per crypto to queryset """
    latest_data = CryptoData.objects.filter(crypto=OuterRef('pk')).order_by('-timestamp')
    return crypto_queryset.annotate(
        invest=Sum(F('purchases__target_price') * F('purchases__amount')),
        amount=Sum('purchases__amount'),
        market_value=Sum(F('purchases__amount') * Subquery(latest_data.values('target_price')[:1])),
        percent_change=(((F('market_value') / F('invest')) * 100) - 100),
        crypto_percent=Subquery(latest_data.values('percent_day')[:1]),
        crypto_value=Subquery(latest_data.values('target_price')[:1]),
    )

def crypto_ohlc(*, crypto: Crypto) -> QuerySet:
    class DateFloor(Func):
        template = "(date_trunc('hour', %(expressions)s) + interval '30 min' * floor(date_part('minute', %(expressions)s) / 30.0))"

    class ArrayHead(Func):
        template = '(%(expressions)s)[1]'

    class ArrayTail(Func):
        template = '(%(expressions)s)[array_upper(%(expressions)s, 1)]'

    crypto.chart = CryptoData.objects.filter(crypto=crypto).values(
        timestampg=DateFloor('timestamp'),
    ).annotate(
        open=ArrayHead(ArrayAgg('target_price')),
        high=Max('target_price'),
        low=Min('target_price'),
        close=ArrayTail(ArrayAgg('target_price')),
    ).order_by('timestampg')

    return crypto
