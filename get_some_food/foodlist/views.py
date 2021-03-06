import datetime

from categories.models import Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, OuterRef, Subquery
from django.db.models.functions import ExtractDay, Coalesce
from django.http import HttpResponseRedirect
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, View, UpdateView, DeleteView, CreateView

from .forms import AddShoppingItemForm, AddProductItemForm, ProductForm, CategoryForm, EditShoppingItemForm
from .models import ShoppingListItem, Purchase, ProductItem, ProductList, Product, ShoppingList


class ToBuyListView(TemplateView):
    template_name = "pages/tobuy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            shopping_list, _ = ShoppingList.objects.get_or_create(owner=self.request.user)
            context['items'] = ShoppingListItem.objects.filter(shopping_list=shopping_list, display=True).order_by(
                'purchased', 'due_date', '-creation_date')
        return context


class PurchaseAjaxView(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        context = {'success': False}
        product_list, _ = ProductList.objects.get_or_create(owner=self.request.user)
        if self.request.is_ajax():
            item_id_str = self.request.POST.get("item_id")
            item = get_object_or_404(ShoppingListItem, pk=int(item_id_str[5:]))
            item.purchased = not item.purchased
            item.save()
            purchases = Purchase.objects.filter(item=item)
            if purchases.exists():
                purchase = purchases[0]
                product_item = ProductItem.objects.get(product=purchase.item.product, product_list=product_list)
                product_item.amount -= purchase.item.amount
                product_item.in_shopping_list = True
                product_item.save()
                purchase.delete()

                context['created'] = False
            else:
                purchase = Purchase(item=item)
                purchase.save()

                product_items = ProductItem.objects.filter(product=purchase.item.product, product_list=product_list)
                if product_items:
                    product_item = product_items[0]
                    product_item.amount += purchase.item.amount
                else:
                    product_item = ProductItem(product=purchase.item.product, amount=purchase.item.amount,
                                               product_list=product_list)

                product_item.in_shopping_list = False
                product_item.save()
                context['created'] = True
            context['success'] = True
        return JsonResponse(context)


class PurchaseHistoryView(ListView):
    model = Purchase
    template_name = "pages/history.html"
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated:
            shopping_list, _ = ShoppingList.objects.get_or_create(owner=self.request.user)
            return Purchase.objects.filter(item__shopping_list=shopping_list).order_by('-buy_date')

        return Purchase.objects.none()


class MyProductsView(ListView):
    model = ProductItem
    template_name = "pages/products.html"
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated:
            product_list, _ = ProductList.objects.get_or_create(owner=self.request.user)
            purchase_date = Purchase.objects.filter(item__product=OuterRef('product')).order_by('-buy_date')

            queryset = ProductItem.objects.filter(product_list=product_list).annotate(
                last_purchased_days=
                ExtractDay(datetime.datetime.today() - Coalesce(Subquery(purchase_date.values('buy_date')[:1]),
                                                                datetime.datetime.today()))
            ).annotate(
                amount_to_warn=F('amount') - F('product__warn_amount')
            ).order_by('-last_purchased_days', 'amount_to_warn')
            return queryset
        return ProductItem.objects.none()


class EditProductView(UpdateView, LoginRequiredMixin):
    model = ProductItem
    template_name = "product_edit.html"
    fields = ["amount"]
    success_url = '/products/'


class DeleteProductView(DeleteView, LoginRequiredMixin):
    model = ProductItem
    success_url = '/products/'


class AddToBuyItemView(CreateView, LoginRequiredMixin):
    template_name = 'add_tobuy_item.html'
    form_class = AddShoppingItemForm
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.shopping_list, _ = ShoppingList.objects.get_or_create(owner=self.request.user)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@login_required
def add_product_to_shopping_list(request, pk):
    shopping_list, _ = ShoppingList.objects.get_or_create(owner=request.user)
    product_item = ProductItem.objects.get(pk=pk)
    shopping_item = ShoppingListItem(shopping_list=shopping_list, product=product_item.product,
                                     amount=product_item.product.default_amount)
    product_item.in_shopping_list = True
    product_item.save()
    shopping_item.save()
    return redirect('/products/')


class AddProductItemView(CreateView, LoginRequiredMixin):
    model = ProductItem
    template_name = 'add_product_item.html'
    success_url = '/products/'
    form_class = AddProductItemForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.product_list = self.product_list
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.product_list, _ = ProductList.objects.get_or_create(owner=self.request.user)
        kwargs['product_list'] = self.product_list
        return kwargs


class EditToBuyView(UpdateView, LoginRequiredMixin):
    model = ShoppingListItem
    template_name = "tobuy_edit.html"
    form_class = EditShoppingItemForm
    success_url = '/'


@login_required
def delete_to_buy_view(request, pk):
    item = get_object_or_404(ShoppingListItem, pk=pk)
    item.display = False
    item.save()
    return redirect('/')


@login_required
def product_create_popup(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        ## Change the value of the "#id_product". This is the element id in the form
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_product");</script>' % (instance.pk, instance))

    return render(request, "product_form.html", {"form": form})


@login_required
def product_edit_popup(request, pk=None):
    instance = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save()
        ## Change the value of the "#id_product". This is the element id in the form

        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_product");</script>' % (instance.pk, instance))

    return render(request, "product_form.html", {"form": form})


@login_required
def category_create_popup(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        ## Change the value of the "#id_category". This is the element id in the form
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_category");</script>' % (instance.pk, instance))

    return render(request, "category_form.html", {"form": form})


@login_required
def category_edit_popup(request, pk=None):
    instance = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save()

        ## Change the value of the "#id_category". This is the element id in the form

        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_category");</script>' % (instance.pk, instance))

    return render(request, "category_form.html", {"form": form})
