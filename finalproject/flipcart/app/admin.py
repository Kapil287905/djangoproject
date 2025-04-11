from django.contrib import admin
from .models import UserDetail,Products,Carts,Orders,Payments

# Register your models here.
class UserDetailAdmin(admin.ModelAdmin):
    list_display = [
        'userid',
        'gender',
        'dob',
        'mobile',
        'address',
        'photo'
    ]

class ProductsAdmin(admin.ModelAdmin):
    list_display = [
        'userid',
        'product_id',
        'product_name',
        'category',
        'description',
        'price',
        'image',
    ]

class CartsAdmin(admin.ModelAdmin):
    list_display = [
        'userid',
        'productid',
        'quantity',
    ]

class OrdersAdmin(admin.ModelAdmin):
    list_display = [
        'orderid',
        'userid',
        'productid',
        'quantity',
        'orderdate',
    ]

class PaymentsAdmin(admin.ModelAdmin):
    list_display = [
        'receiptid',
        'orderid',
        'userid',
        'productid',
        'paymenttype',
        'paymentstatus',
    ]

admin.site.register(UserDetail,UserDetailAdmin)
admin.site.register(Products,ProductsAdmin)
admin.site.register(Carts,CartsAdmin)
admin.site.register(Orders,OrdersAdmin)
admin.site.register(Payments,PaymentsAdmin)