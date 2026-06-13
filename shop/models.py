from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name_zh = models.CharField(_("Name (Chinese)"), max_length=100)
    name_en = models.CharField(_("Name (English)"), max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(_("Category Image"), upload_to="categories/", blank=True)
    order = models.IntegerField(_("Order"), default=0)
    is_active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("分类")
        verbose_name_plural = _("分类")
        ordering = ["order", "id"]

    def __str__(self):
        return self.name_zh


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name="products", verbose_name=_("分类")
    )
    name_zh = models.CharField(_("Name (Chinese)"), max_length=200)
    name_en = models.CharField(_("Name (English)"), max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(_("Main Image"), upload_to="products/", blank=True)
    specs_zh = models.TextField(_("Specs (Chinese)"), blank=True)
    specs_en = models.TextField(_("Specs (English)"), blank=True)
    desc_zh = models.TextField(_("Description (Chinese)"), blank=True)
    desc_en = models.TextField(_("Description (English)"), blank=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    stock = models.IntegerField(_("Stock"), default=0)
    is_featured = models.BooleanField(_("Featured"), default=False)
    is_active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_featured", "is_active"]),
        ]

    def __str__(self):
        return self.name_zh


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="images", verbose_name=_("Product")
    )
    image = models.ImageField(_("Image"), upload_to="products/gallery/")
    order = models.IntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ["order"]


class Customer(models.Model):
    name = models.CharField(_("Contact Name"), max_length=100)
    company = models.CharField(_("Company"), max_length=200, blank=True)
    email = models.EmailField(_("Email"), unique=True)
    phone = models.CharField(_("Phone"), max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return f"{self.name} ({self.company})"


class Address(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
        related_name="addresses", verbose_name=_("Customer")
    )
    address_zh = models.CharField(_("Address (Chinese)"), max_length=500)
    address_en = models.CharField(_("Address (English)"), max_length=500, blank=True)
    city = models.CharField(_("City"), max_length=100)
    country = models.CharField(_("Country"), max_length=100, default="China")
    zip_code = models.CharField(_("Zip Code"), max_length=20, blank=True)
    is_default = models.BooleanField(_("Default Address"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")


class Cart(models.Model):
    session_id = models.CharField(_("Session"), max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def item_count(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE,
        related_name="items", verbose_name=_("Cart")
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_PROCESSING = "processing"
    STATUS_SHIPPED = "shipped"
    STATUS_DELIVERED = "delivered"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, _("Pending")),
        (STATUS_PAID, _("Paid")),
        (STATUS_PROCESSING, _("Processing")),
        (STATUS_SHIPPED, _("Shipped")),
        (STATUS_DELIVERED, _("Delivered")),
        (STATUS_CANCELLED, _("Cancelled")),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name=_("Customer")
    )
    customer_name = models.CharField(_("Contact Name"), max_length=100)
    customer_email = models.EmailField(_("Email"))
    customer_phone = models.CharField(_("Phone"), max_length=50, blank=True)
    shipping_address = models.TextField(_("Shipping Address"))
    status = models.CharField(
        _("Status"), max_length=20,
        choices=STATUS_CHOICES, default=STATUS_PAID
    )
    total = models.DecimalField(_("Total"), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name="items", verbose_name=_("Order")
    )
    product_name = models.CharField(_("Product Name"), max_length=200)
    product_price = models.DecimalField(_("Unit Price"), max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(_("Quantity"))
    subtotal = models.DecimalField(_("Subtotal"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")


class ContactInquiry(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    company = models.CharField(_("Company"), max_length=200, blank=True)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=50, blank=True)
    product = models.CharField(_("Product"), max_length=200, blank=True)
    message = models.TextField(_("Message"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Inquiry")
        verbose_name_plural = _("Inquiries")
        ordering = ["-created_at"]
