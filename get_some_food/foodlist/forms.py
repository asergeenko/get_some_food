# from django.db import models
from categories.models import Category
from django.forms import ModelForm

from .models import ShoppingListItem, ShoppingList, Product, ProductItem


class AddShoppingItemForm(ModelForm):
    class Meta:
        model = ShoppingListItem
        exclude = ['due_date', 'shopping_list', 'purchased', 'display']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddShoppingItemForm, self).__init__(*args, **kwargs)
        shopping_list, _ = ShoppingList.objects.get_or_create(owner=user)
        product_ids = list(
            ShoppingListItem.objects.filter(shopping_list=shopping_list).values_list('product__pk', flat=True))
        self.fields['product'].queryset = Product.objects.exclude(pk__in=product_ids)
        self.fields['product'].widget.attrs.update({'class': 'form-control mr-2'})


class AddProductItemForm(ModelForm):
    class Meta:
        model = ProductItem
        fields = ['product', 'amount']

    def __init__(self, *args, **kwargs):
        product_list = kwargs.pop('product_list')
        super().__init__(*args, **kwargs)
        product_ids = list(
            ProductItem.objects.filter(product_list=product_list).values_list('product__pk', flat=True))

        self.fields['product'].queryset = Product.objects.exclude(pk__in=product_ids)
        self.fields['product'].widget.attrs.update({'class': 'form-control mr-2'})


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control mr-2'})


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'parent']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.exclude(pk=kwargs['instance'].pk)
