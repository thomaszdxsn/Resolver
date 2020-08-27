from django.contrib import admin
from .models import Card, Transaction, Merchant


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    pass


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
