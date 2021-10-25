from django.contrib import admin
from django.db import models
from django.conf import settings

# Create your models here.
from django.utils import timezone
from forex_python.converter import CurrencyRates, CurrencyCodes, RatesNotAvailableError

from crypto.utils import crypto_image_path


class Crypto(models.Model):
    symbol = models.CharField(max_length=10, help_text='Crypto Ticker used for querying from CoinMarketCap')
    display_name = models.CharField(max_length=64, help_text='Used as the header when charting')
    show_overall = models.BooleanField(default=False, help_text='Show overall value instead of current price')
    show_chart = models.BooleanField(default=False, verbose_name='Chart crypto', help_text='Show 7-day chart with price trend on Dashboard')
    image = models.ImageField(default='crypto/default.png', upload_to=crypto_image_path)
    enabled = models.BooleanField(default=True, help_text='Hides crypto from Dashboard and does not pull further information')
    order = models.PositiveSmallIntegerField(default=999)
    updated = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('order', 'symbol')

    def __str__(self):
        return self.symbol

    @property
    def market_valuex(self):
        purchase_amount = sum([p.amount * p.target_price for p in self.purchases.all()])
        market_value = purchase_amount * self.data.all()[:1][0].target_price
        return purchase_amount


class CryptoData(models.Model):
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE, related_name='data')
    source_price = models.FloatField()
    source_currency = models.CharField(max_length=4)
    target_price = models.FloatField()
    target_currency = models.CharField(max_length=4)
    percent_day = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='24h Percentual Change')
    rank = models.PositiveIntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Price Data'
        verbose_name_plural = 'Price Data'
        get_latest_by = 'timestamp'

    def save(self, *args, **kwargs):
        if not self.target_price:
            # Converts currency to target currency because CoinMarket's integrated conversion sucks
            from crypto.services import currency_convert
            self.target_currency = settings.TARGET_CURRENCY or settings.COINMARKET_CURRENCY
            self.target_price = currency_convert(
                source_currency=self.source_currency,
                target_currency=self.target_currency,
                source_amount=self.source_price
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f'[{self.crypto}] {self.price}@{self.timestamp}'

    @property
    @admin.display(
        ordering='target_price',
        description='Price',
    )
    def price(self) -> str:
        c = CurrencyCodes()
        symbol = c.get_symbol(self.target_currency)
        return f'{self.target_price:.20f} {symbol}'

    @property
    @admin.display(
        ordering='percent_day',
        description='24h percentual',
    )
    def percent(self) -> str:
        return f'{self.percent_day:+.2f} %'


class CryptoPurchases(models.Model):
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE, related_name='purchases')
    amount = models.FloatField()
    buy_price = models.FloatField(blank=True, help_text='If no buy price is specified, it will be looked up on '
                                                      'CoinMarketCap based on the buying timestamp (requires Advanced API plan)')
    buy_currency = models.CharField(max_length=4)
    target_price = models.FloatField()
    target_currency = models.CharField(max_length=4)
    bought_at = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        verbose_name = 'Purchase'

    def save(self, *args, **kwargs):
        if not self.pk and not self.buy_currency:
            self.buy_currency = settings.TARGET_CURRENCY or settings.COINMARKET_CURRENCY

        if not self.target_price:
            from crypto.services import currency_convert
            self.target_currency = settings.TARGET_CURRENCY or settings.COINMARKET_CURRENCY
            self.target_price = currency_convert(
                source_currency=self.buy_currency,
                target_currency=self.target_currency,
                source_amount=self.buy_price,
                timestamp=self.bought_at
            )

        super().save(*args, **kwargs)

    @property
    def total_price(self):
        c = CurrencyCodes()
        symbol = c.get_symbol(self.target_currency)
        return f'{(self.amount*self.target_price):.2f} {symbol}'


class Alert(models.Model):
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    price = models.FloatField(help_text='Price of crypto in target currency to surpass')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Price Alert'

    def __str__(self):
        return f'[{self.crypto}] {self.price}'
