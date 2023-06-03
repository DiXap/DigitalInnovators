from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=200, unique=True, primary_key=True)

    def __str__(self) -> str:
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name}: {self.category}'

class CartItem(models.Model):
    time = models.DateTimeField(auto_now_add=True)

    item  = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='item')
    table = models.ForeignKey(User, on_delete=models.CASCADE, related_name='table')


    def __str__(self) -> str:
        return f'{self.table.username} - {self.item.name} @ {self.time}'


class KitchenOrder(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    order = models.TextField(blank=True)

    table = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return f'{self.table} @ {self.time}'

class Sale(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    order = models.TextField(blank=True)
    sale = models.DecimalField(max_digits=7, decimal_places=2)    

    table = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.table} - {self.sale} @ {self.time}'


class Comensal(models.Model):
    name = models.CharField(max_length=100)
    table = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name} @ {self.table}'

class Helado(models.Model):
    table = models.ForeignKey(User, on_delete=models.CASCADE)
    flavour = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.flavour} @ {self.table}'