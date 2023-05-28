from django.db import models

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=200, unique=True, primary_key=True)

    def __str__(self) -> str:
        return self.name