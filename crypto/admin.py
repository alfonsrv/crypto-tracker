from django.contrib import admin

from crypto.models import Crypto, CryptoData, CryptoPurchases, Alert


@admin.register(Crypto)
class CryptoAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'display_name', 'updated', 'enabled')
    ordering = ('symbol',)


@admin.register(CryptoData)
class CryptoDataAdmin(admin.ModelAdmin):
    list_display = ('crypto', 'price', 'percent', 'timestamp')
    ordering = ('-timestamp', 'crypto')
    readonly_fields = ('timestamp',)


@admin.register(CryptoPurchases)
class CryptoPurchasesAdmin(admin.ModelAdmin):
    list_display = ('crypto', 'amount', 'buy_price', 'total_price', 'bought_at')
    ordering = ('-bought_at',)


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('crypto', 'price')
    ordering = ('timestamp',)
