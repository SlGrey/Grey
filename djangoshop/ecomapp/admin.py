from django.contrib import admin
from ecomapp.models import (
    Category,
    Brand,
    Product,
    CartItem,
    Cart,
    Order,
)


def make_payed(modeladmin, request, queryset):
    queryset.update(status="Оплачен")
    make_payed.short_description = "Пометить как оплаченый"


def make_in_progres(ModelAdmn, request, queryset):
    queryset.update(status="Выполняется")
    make_payed.short_description = "Пометить как выполняется"


class OrderAdmin(admin.ModelAdmin):
    list_filter = ["status"]
    actions = [make_in_progres, make_payed]


# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
