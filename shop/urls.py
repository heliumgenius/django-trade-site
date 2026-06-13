from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("products/<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/add/<int:product_id>/", views.AddToCartView.as_view(), name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.RemoveFromCartView.as_view(), name="remove_from_cart"),
    path("cart/update/<int:item_id>/", views.UpdateCartView.as_view(), name="update_cart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("checkout/success/<int:order_id>/", views.OrderSuccessView.as_view(), name="order_success"),
    path("orders/", views.OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
]
