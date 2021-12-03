from django.contrib import admin

# Register your models here.
from get_some_food.foodlist import models

admin.site.register(models.Unit)
admin.site.register(models.Product)
admin.site.register(models.Purchase)
admin.site.register(models.ShoppingListItem)
admin.site.register(models.ShoppingList)
admin.site.register(models.ProductItem)
admin.site.register(models.ProductList)
