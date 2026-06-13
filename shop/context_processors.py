from .models import Category
from .cart import get_cart


def global_settings(request):
    categories = Category.objects.filter(is_active=True).order_by("order")
    cart = get_cart(request)
    return {
        "site_categories": categories,
        "cart_count": cart.item_count(),
        "cart_total": cart.total(),
    }
