from django.contrib import admin
from .models import (
    Category, Product, ProductImage,
    Customer, Address,
    Cart, CartItem,
    Order, OrderItem,
    ContactInquiry,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ["product_name", "product_price", "quantity", "subtotal"]
    can_delete = False
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name_zh", "name_en", "order", "is_active"]
    list_editable = ["order", "is_active"]
    prepopulated_fields = {"slug": ("name_en",)}
    search_fields = ["name_zh", "name_en"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name_zh", "category", "price", "stock", "is_featured", "is_active"]
    list_filter = ["category", "is_featured", "is_active"]
    search_fields = ["name_zh", "name_en"]
    prepopulated_fields = {"slug": ("name_en",)}
    inlines = [ProductImageInline]
    list_editable = ["price", "stock", "is_featured", "is_active"]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "image", "order"]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "company", "email", "phone", "created_at"]
    search_fields = ["name", "company", "email"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["customer", "city", "country", "is_default"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer_name", "customer_email", "total", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["customer_name", "customer_email"]
    inlines = [OrderItemInline]
    readonly_fields = ["total", "created_at"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product_name", "quantity", "subtotal"]
    readonly_fields = ["product_name", "product_price", "quantity", "subtotal"]


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ["name", "company", "email", "created_at"]
    readonly_fields = ["name", "company", "email", "phone", "product", "message", "created_at"]


admin.site.register(Cart)
admin.site.register(CartItem)
