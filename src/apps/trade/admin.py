from django.contrib import admin

from apps.trade.models import OpenOrder


class AdminOpenOrderView(admin.ModelAdmin):
    list_display = ("__str__",)
    

admin.site.register(OpenOrder, AdminOpenOrderView)