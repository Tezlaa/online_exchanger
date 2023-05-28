from django.contrib import admin
from exchange.models import FactorPrice, Currency, Banks, OffersData, SettingUpWebSite


class AdminCurrency(admin.ModelAdmin):
    """View and settings up limits for the currency"""
    
    list_display = ('currency', 'get_his_banks', 'min_value', 'max_value')
    filter_horizontal = ('his_banks', )
    list_editable = ('min_value', 'max_value',)
    list_filter = ('currency', )
    

class AdminBanks(admin.ModelAdmin):
    """View and settings up limits for the currency"""
    
    list_display = ('bank_name', 'limit_bank',)
    list_editable = ('bank_name', 'limit_bank',)
    list_display_links = None


class AdminOfferData(admin.ModelAdmin):
    """View all offer in the admin interface"""
    
    list_display = ('id_order', 'time_create', 'currency_get', 'how_many_get', 'currency_take')
    list_filter = ('time_create', 'currency_get', 'how_many_get', 'currency_take')
    search_fields = ('currency_get', 'currency_take', 'bank_get', 'bank_take')


class AdminFactorPrice(admin.ModelAdmin):
    """View and settings up factor for currency"""

    list_display = ('fiat_buy', 'factor_buy', 'fiat_sell', 'factor_sell')
    list_filter = ('fiat_buy', 'fiat_sell')
    search_fields = ('fiat_buy', 'fiat_sell')


class AdminSettingUpWebSite(admin.ModelAdmin):
    all_fields = ('link_tg', 'number_viber', 'link_whatsapp', 'visible_parimatch')
    
    list_display = all_fields
    list_editable = all_fields
    list_display_links = None
    

class AdminAllOrder(admin.ModelAdmin):
    """ View all order in the exchange site """
    
    list_display = ('id_order', 'time_create', 'currency_get', 'how_many_get', 'currency_take')
    list_filter = ('time_create', 'currency_get', 'how_many_get', 'currency_take')
    search_fields = ('currency_get', 'currency_take', 'bank_get', 'bank_take')


admin.site.register(Banks, AdminBanks)
admin.site.register(Currency, AdminCurrency)
admin.site.register(FactorPrice, AdminFactorPrice)
admin.site.register(SettingUpWebSite, AdminSettingUpWebSite)
admin.site.register(OffersData, AdminAllOrder)