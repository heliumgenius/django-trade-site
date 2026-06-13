from django.db import transaction
from .models import Order, OrderItem, Customer
from .cart import get_cart, clear_cart


@transaction.atomic
def create_order(request, form_data):
    cart = get_cart(request)
    if cart.item_count() == 0:
        return None

    email = form_data.get("email", "").strip().lower()
    customer, _created = Customer.objects.get_or_create(
        email=email,
        defaults={
            "name": form_data.get("name", ""),
            "company": form_data.get("company", ""),
            "phone": form_data.get("phone", ""),
        },
    )

    address_parts = [
        form_data.get("address", ""),
        form_data.get("city", ""),
        form_data.get("country", "China"),
    ]
    address_text = ", ".join(p for p in address_parts if p)

    total = sum(item.product.price * item.quantity for item in cart.items.all())

    order = Order.objects.create(
        customer=customer,
        customer_name=form_data.get("name", ""),
        customer_email=email,
        customer_phone=form_data.get("phone", ""),
        shipping_address=address_text,
        total=total,
        status=Order.STATUS_PAID,
    )

    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product_name=cart_item.product.name_en,
            product_price=cart_item.product.price,
            quantity=cart_item.quantity,
            subtotal=cart_item.product.price * cart_item.quantity,
        )
        product = cart_item.product
        product.stock = max(0, product.stock - cart_item.quantity)
        product.save()

    clear_cart(request)
    return order
