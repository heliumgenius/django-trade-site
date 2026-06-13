import uuid
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Product


def get_cart(request):
    if hasattr(request, "_cart"):
        return request._cart
    session_id = request.session.get("cart_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session["cart_id"] = session_id
        request.session.set_expiry(60 * 60 * 24 * 7)
        cart = Cart.objects.create(session_id=session_id)
    else:
        cart, _created = Cart.objects.get_or_create(session_id=session_id)
    request._cart = cart
    return cart


def add_to_cart(request, product_id, quantity=1):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    item, _created = CartItem.objects.get_or_create(
        cart=cart, product=product, defaults={"quantity": 0},
    )
    item.quantity += quantity
    item.save()
    return cart


def remove_from_cart(request, item_id):
    cart = get_cart(request)
    CartItem.objects.filter(id=item_id, cart=cart).delete()


def update_quantity(request, item_id, quantity):
    cart = get_cart(request)
    if quantity <= 0:
        CartItem.objects.filter(id=item_id, cart=cart).delete()
    else:
        CartItem.objects.filter(id=item_id, cart=cart).update(quantity=quantity)


def clear_cart(request):
    cart = get_cart(request)
    cart.items.all().delete()
