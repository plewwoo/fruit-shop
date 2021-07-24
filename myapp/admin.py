from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = 'Fruit Shop Admin'
admin.site.index_title = 'Main Admin'
admin.site.site_title = 'Fruit Shop Backend'


class AllProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'instock']
    list_editable = ['price', 'quantity', 'instock']
    list_filter = ['instock']
    search_fields = ['name']


admin.site.register(AllProduct, AllProductAdmin)
admin.site.register(Profile)
admin.site.register(Cart)


class OrderListAdmin(admin.ModelAdmin):
    list_display = ['orderId', 'productName', 'total']


admin.site.register(OrderList, OrderListAdmin)


class OrderPendingAdmin(admin.ModelAdmin):
    list_display = ['orderId', 'user', 'paid', 'slip']
    list_filter = ['paid']


admin.site.register(OrderPending, OrderPendingAdmin)
