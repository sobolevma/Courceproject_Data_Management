from django.contrib import admin
from ecomapp.models import Category, Brand, Service, Phone, CartItem, Cart, Order

# Register your models here.

def make_payed(modeladmin, request, queryset):
    queryset.update(status='Оплачен')
make_payed.short_description = "Пометить как оплаченные"

def make_is_performing(modeladmin, request, queryset):
    queryset.update(status='Выполняется')
make_is_performing.short_description = "Пометить как выполняющийся"

class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    actions = [make_is_performing, make_payed]


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Service)
admin.site.register(Phone)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)