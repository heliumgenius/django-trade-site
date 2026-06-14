from django.test import TestCase
from django.urls import reverse
from shop.models import Category, Product, Customer, Order, Cart, CartItem, ContactInquiry
from shop.forms import CheckoutForm, ContactForm


class CategoryModelTest(TestCase):
    def test_create_category(self):
        c = Category.objects.create(name_zh="加工中心", name_en="Machining Center", slug="machining-center")
        self.assertEqual(str(c), "加工中心")

    def test_slug_unique(self):
        Category.objects.create(name_zh="a", name_en="a", slug="test")
        with self.assertRaises(Exception):
            Category.objects.create(name_zh="b", name_en="b", slug="test")

    def test_ordering(self):
        c1 = Category.objects.create(name_zh="B", name_en="B", slug="b", order=2)
        c2 = Category.objects.create(name_zh="A", name_en="A", slug="a", order=1)
        self.assertEqual(list(Category.objects.all()), [c2, c1])


class ProductModelTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name_zh="加工中心", name_en="MC", slug="mc")

    def test_create_product(self):
        p = Product.objects.create(category=self.cat, name_zh="立式加工中心", name_en="VMC", slug="vmc", price=50000, stock=10)
        self.assertEqual(str(p), "立式加工中心")
        self.assertTrue(p.is_active)

    def test_slug_unique(self):
        Product.objects.create(category=self.cat, name_zh="a", name_en="a", slug="test", price=1)
        with self.assertRaises(Exception):
            Product.objects.create(category=self.cat, name_zh="b", name_en="b", slug="test", price=1)


class CustomerModelTest(TestCase):
    def test_create_customer(self):
        c = Customer.objects.create(name="John", company="ACME", email="john@acme.com")
        self.assertEqual(str(c), "John (ACME)")

    def test_email_unique(self):
        Customer.objects.create(name="A", email="a@b.com")
        with self.assertRaises(Exception):
            Customer.objects.create(name="B", email="a@b.com")


class OrderModelTest(TestCase):
    def test_create_order(self):
        o = Order.objects.create(customer_name="John", customer_email="j@a.com", shipping_address="123 St", total=100)
        self.assertIn("Order #", str(o))
        self.assertEqual(o.status, Order.STATUS_PAID)

    def test_status_choices(self):
        self.assertEqual(len(Order.STATUS_CHOICES), 6)


class CartTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name_zh="a", name_en="a", slug="a")
        self.product = Product.objects.create(category=self.cat, name_zh="p", name_en="p", slug="p", price=100, stock=10)

    def test_cart_total(self):
        cart = Cart.objects.create(session_id="test-session")
        CartItem.objects.create(cart=cart, product=self.product, quantity=3)
        self.assertEqual(cart.total(), 300)

    def test_cart_item_count(self):
        cart = Cart.objects.create(session_id="test-session")
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        self.assertEqual(cart.item_count(), 3)

    def test_cartitem_subtotal(self):
        cart = Cart.objects.create(session_id="test-session")
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=5)
        self.assertEqual(item.subtotal(), 500)


class ContactInquiryTest(TestCase):
    def test_create_inquiry(self):
        i = ContactInquiry.objects.create(name="John", email="j@a.com", message="Hello")
        self.assertEqual(i.name, "John")


class HomeViewTest(TestCase):
    def test_home_200(self):
        self.assertEqual(self.client.get(reverse("shop:home")).status_code, 200)

    def test_home_template(self):
        self.assertTemplateUsed(self.client.get(reverse("shop:home")), "index.html")


class ProductListViewTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name_zh="a", name_en="a", slug="a")
        self.p1 = Product.objects.create(category=self.cat, name_zh="p1", name_en="p1", slug="p1", price=10, is_active=True)
        self.p2 = Product.objects.create(category=self.cat, name_zh="p2", name_en="p2", slug="p2", price=20, is_active=False)

    def test_product_list_200(self):
        self.assertEqual(self.client.get(reverse("shop:product_list")).status_code, 200)

    def test_filter_by_category(self):
        resp = self.client.get(reverse("shop:product_list") + "?category=a")
        self.assertContains(resp, "p1")
        self.assertNotContains(resp, "p2")

    def test_search(self):
        resp = self.client.get(reverse("shop:product_list") + "?q=p1")
        self.assertContains(resp, "p1")

    def test_empty_search(self):
        resp = self.client.get(reverse("shop:product_list") + "?q=nonexistent")
        self.assertContains(resp, "No products found")


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name_zh="a", name_en="a", slug="a")
        self.p = Product.objects.create(category=self.cat, name_zh="p", name_en="p", slug="p", price=10, is_active=True)

    def test_detail_200(self):
        self.assertEqual(self.client.get(reverse("shop:product_detail", args=["p"])).status_code, 200)

    def test_detail_404(self):
        self.assertEqual(self.client.get(reverse("shop:product_detail", args=["x"])).status_code, 404)


class CartViewTest(TestCase):
    def test_cart_200(self):
        self.assertEqual(self.client.get(reverse("shop:cart")).status_code, 200)


class CheckoutViewTest(TestCase):
    def test_checkout_get_redirects_empty(self):
        self.assertEqual(self.client.get(reverse("shop:checkout")).status_code, 302)


class ContactViewTest(TestCase):
    def test_contact_get_200(self):
        self.assertEqual(self.client.get(reverse("shop:contact")).status_code, 200)

    def test_contact_post_valid(self):
        resp = self.client.post(reverse("shop:contact"), {"name": "John", "email": "j@a.com", "message": "Hi"})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(ContactInquiry.objects.count(), 1)

    def test_contact_post_invalid(self):
        resp = self.client.post(reverse("shop:contact"), {"name": "", "email": "", "message": ""})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(ContactInquiry.objects.count(), 0)


class AboutViewTest(TestCase):
    def test_about_200(self):
        self.assertEqual(self.client.get(reverse("shop:about")).status_code, 200)


class OrderListViewTest(TestCase):
    def test_order_list_200(self):
        self.assertEqual(self.client.get(reverse("shop:order_list")).status_code, 200)


class CheckoutFormTest(TestCase):
    def test_valid(self):
        f = CheckoutForm({"name": "John", "email": "j@a.com", "address": "123 St"})
        self.assertTrue(f.is_valid())

    def test_missing_required(self):
        f = CheckoutForm({"name": "", "email": "", "address": ""})
        self.assertFalse(f.is_valid())


class ContactFormTest(TestCase):
    def test_valid(self):
        f = ContactForm({"name": "John", "email": "j@a.com", "message": "Hi"})
        self.assertTrue(f.is_valid())

    def test_missing_required(self):
        f = ContactForm({"name": "", "email": "", "message": ""})
        self.assertFalse(f.is_valid())


class AddToCartViewTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name_zh="a", name_en="a", slug="a")
        self.product = Product.objects.create(category=self.cat, name_zh="p", name_en="p", slug="p", price=100, stock=10)

    def test_add_to_cart_redirects(self):
        resp = self.client.post(reverse("shop:add_to_cart", args=[self.product.id]), {"quantity": 2})
        self.assertEqual(resp.status_code, 302)
