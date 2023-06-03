from django.contrib import admin

from .models import Categories, Menu, CartItem, KitchenOrder, Sale, Comensal

# Register your models here.
admin.site.register(Categories)
admin.site.register(Menu)
admin.site.register(CartItem)
admin.site.register(KitchenOrder)
admin.site.register(Sale)
admin.site.register(Comensal)