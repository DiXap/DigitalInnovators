from django.contrib import admin

from .models import Categories, Menu, CartItem

# Register your models here.
admin.site.register(Categories)
admin.site.register(Menu)
admin.site.register(CartItem)