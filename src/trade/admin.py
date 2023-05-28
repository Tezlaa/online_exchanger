from django.contrib import admin

from trade.models import OpenOrder


class AdminOpenOrderView(admin.ModelAdmin):
    list_display = ("__str__",)
    

admin.site.register(OpenOrder, AdminOpenOrderView)