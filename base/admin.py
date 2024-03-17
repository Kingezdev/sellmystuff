from django.contrib import admin
from .models import Product, Message, Cart, Shop

# Register your models here.
admin.site.register(Product)
admin.site.register(Message)
admin.site.register(Cart)
admin.site.register(Shop)