from django.urls import path

from get_some_food.foodlist.views import (
    ToBuyListView,
    PurchaseHistoryView,
    MyProductsView,
    PurchaseAjaxView,
    EditProductView,
    DeleteProductView,
    AddToBuyItemView,
    add_product_to_shopping_list,
    AddProductItemView,
    EditToBuyView,
    delete_to_buy_view,
    product_edit_popup,
    product_create_popup,
    category_edit_popup,
    category_create_popup,
)

app_name = "foodlist"

urlpatterns = [
    path("", ToBuyListView.as_view(), name="list"),
    path("products/", MyProductsView.as_view(), name="products"),
    path("history/", PurchaseHistoryView.as_view(), name="history"),
    path("purchase/", PurchaseAjaxView.as_view(), name="purchase"),
    path("products/edit/<int:pk>/", EditProductView.as_view(), name="edit_product"),
    path("products/delete/<int:pk>/", DeleteProductView.as_view(), name="delete_product"),

    path("product/<int:pk>/edit/", product_edit_popup, name="product_edit_popup"),
    path("product/create/", product_create_popup, name="product_create_popup"),

    path("category/<int:pk>/edit/", category_edit_popup, name="category_edit_popup"),
    path("category/create/", category_create_popup, name="category_create_popup"),

    path("tobuy/edit/<int:pk>/", EditToBuyView.as_view(), name="edit_tobuy"),
    path("tobuy/delete/<int:pk>/", delete_to_buy_view, name="delete_tobuy"),

    path("add-shopping-item/", AddToBuyItemView.as_view(), name="add_shopping_item"),
    path("add-product-to-list/<int:pk>/", add_product_to_shopping_list, name="add_product_to_shopping_list"),
    path("add-product-item/", AddProductItemView.as_view(), name="add_product_item"),
]
