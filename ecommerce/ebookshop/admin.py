from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Products)
admin.site.register(Customer)
#admin.site.register(Order)
#admin.site.register(OrderItem)
#admin.site.register(ShippingAddress)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','complete','transaction_id','status')
    ordering = ('date_ordered',)
    search_fields =('complete','transaction_id')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order','product','quantity')
    list_filter =('order',)
    search_fields = ('order__id',)

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('order','customer')
