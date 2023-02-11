from django.contrib import admin
from .models import Product, Category, Order, Cart
from django.utils.html import format_html
# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'date', 'status', 'shipping_status']
    ordering = ('-status',) 
    search_fields = ('code', )

class SeminarInline(admin.StackedInline):
    model = Order
    extra = 0
    ordering = ('status',)    

    def image_tag(self, obj):
        return format_html('<img src="{}" width="auto" height="200px" />'.format(obj.image.url))
    image_tag.short_description = 'Product Image Preview'
    readonly_fields = ['image_tag']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)