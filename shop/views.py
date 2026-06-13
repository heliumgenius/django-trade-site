from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import get_language

from .models import Category, Product, Order, ContactInquiry
from .cart import get_cart, add_to_cart, remove_from_cart, update_quantity
from .checkout import create_order
from .forms import CheckoutForm, ContactForm


class HomeView(View):
    def get(self, request):
        categories = Category.objects.filter(is_active=True)
        featured = Product.objects.filter(
            is_featured=True, is_active=True
        ).select_related("category")[:8]
        return render(request, "index.html", {
            "categories": categories,
            "featured_products": featured,
        })


class ProductListView(View):
    def get(self, request):
        products = Product.objects.filter(is_active=True).select_related("category")
        category_slug = request.GET.get("category")
        search_query = request.GET.get("q", "").strip()

        if category_slug:
            products = products.filter(category__slug=category_slug)
        if search_query:
            lang = get_language()
            if lang and lang.startswith("zh"):
                products = products.filter(name_zh__icontains=search_query)
            else:
                products = products.filter(name_en__icontains=search_query)

        categories = Category.objects.filter(is_active=True)
        current_category = None
        if category_slug:
            current_category = Category.objects.filter(slug=category_slug).first()

        return render(request, "shop/product_list.html", {
            "products": products,
            "categories": categories,
            "current_category": current_category,
            "search_query": search_query,
        })


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(
            Product.objects.select_related("category"), slug=slug, is_active=True
        )
        related = Product.objects.filter(
            category=product.category, is_active=True
        ).exclude(id=product.id)[:4]
        return render(request, "shop/product_detail.html", {
            "product": product,
            "related_products": related,
        })


class CartView(View):
    def get(self, request):
        cart = get_cart(request)
        return render(request, "shop/cart.html", {"cart": cart})


class AddToCartView(View):
    def post(self, request, product_id):
        try:
            quantity = int(request.POST.get("quantity", 1))
        except (ValueError, TypeError):
            quantity = 1
        add_to_cart(request, product_id, max(1, quantity))
        return redirect("shop:cart")


class RemoveFromCartView(View):
    def post(self, request, item_id):
        remove_from_cart(request, item_id)
        return redirect("shop:cart")


class UpdateCartView(View):
    def post(self, request, item_id):
        try:
            quantity = int(request.POST.get("quantity", 1))
        except (ValueError, TypeError):
            quantity = 1
        update_quantity(request, item_id, quantity)
        return redirect("shop:cart")


class CheckoutView(View):
    def get(self, request):
        cart = get_cart(request)
        if cart.item_count() == 0:
            return redirect("shop:cart")
        form = CheckoutForm()
        return render(request, "shop/checkout.html", {"form": form, "cart": cart})

    def post(self, request):
        cart = get_cart(request)
        if cart.item_count() == 0:
            return redirect("shop:cart")
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = create_order(request, form.cleaned_data)
            if order:
                return redirect("shop:order_success", order_id=order.id)
        return render(request, "shop/checkout.html", {"form": form, "cart": cart})


class OrderSuccessView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, "shop/order_success.html", {"order": order})


class OrderListView(View):
    def get(self, request):
        email = request.GET.get("email", "").strip().lower()
        orders = []
        if email:
            orders = Order.objects.filter(customer_email=email)
        return render(request, "shop/order_list.html", {
            "orders": orders, "search_email": email,
        })

    def post(self, request):
        email = request.POST.get("email", "").strip().lower()
        return redirect(f"{reverse('shop:order_list')}?email={email}")


class OrderDetailView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        return render(request, "shop/order_detail.html", {"order": order})


class AboutView(View):
    def get(self, request):
        return render(request, "shop/about.html")


class ContactView(View):
    def get(self, request):
        return render(request, "shop/contact.html", {"form": ContactForm()})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactInquiry.objects.create(**form.cleaned_data)
            messages.success(request, "Your inquiry has been received!")
            return redirect("shop:contact")
        return render(request, "shop/contact.html", {"form": form})
