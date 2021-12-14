from categories.models import Category
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Unit(models.Model):
    '''Units of measurement'''
    short_name = models.CharField(max_length=30)
    long_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.long_name} ({self.short_name})'


class Product(models.Model):
    name = models.CharField(max_length=255)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # срок годности
    shelf_life = models.DurationField(null=True, blank=True)
    # количество продукта, при котором нужно предупреждать о необходимости купить новый
    warn_amount = models.FloatField(default=1.0)
    # Для яиц - 10
    default_amount = models.FloatField(default=1.0)

    def __str__(self):
        return f'{self.name} ({self.unit.short_name})'


class ShoppingList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name='shopping_lists', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.creation_date.strftime("%d-%m-%Y %H:%M")} {self.owner.username}'


class ShoppingListItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.FloatField(default=1.0)
    comment = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    purchased = models.BooleanField(default=False)
    display = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.product}: {self.amount} {self.product.unit.short_name}. {self.comment}'

    def save(self, *args, **kwargs):
        if self.amount < 0:
            self.amount = 0
        super().save(*args, **kwargs)


class Purchase(models.Model):
    item = models.ForeignKey(ShoppingListItem, on_delete=models.CASCADE)
    buy_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.buy_date.strftime("%d-%m-%Y %H:%M")} {self.item}'


class ProductList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name='product_lists', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.creation_date.strftime("%d-%m-%Y %H:%M")} {self.owner.username}'


class ProductItem(models.Model):
    product_list = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    in_shopping_list = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product} {self.amount} {self.product.unit.short_name}'

    def save(self, *args, **kwargs):
        if self.amount < 0:
            self.amount = 0
        super().save(*args, **kwargs)
