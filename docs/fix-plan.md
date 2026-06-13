# Fix Plan — django-trade-site

## 执行顺序：从上到下依次修，每修完一步再动下一步。

---

### 1. 删除残留文件

删除项目根目录的 `_b64writer.py`。

### 2. 创建 `.env.example`

在项目根目录创建 `.env.example`，内容：
```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 3. 修复 requirements.txt 版本

`requirements.txt` 第 1 行：`Django~=5.1.0` → `Django~=6.0.0`

### 4. 移除弃用设置

`config/settings.py:75`：删除 `USE_L10N = True` 这一行。

### 5. 结账和联系表单显示验证错误

**文件：`templates/shop/checkout.html`**
在 `<form method="post">{% csrf_token %}` 之后、`<div class="row g-3">` 之前添加：
```html
{% if form.errors %}<div class="alert alert-danger">{% for field in form %}{% for err in field.errors %}{{ err }}<br>{% endfor %}{% endfor %}{% for err in form.non_field_errors %}{{ err }}<br>{% endfor %}</div>{% endif %}
```

**文件：`templates/shop/contact.html`**
在 `<form method="post">{% csrf_token %}` 之后、`<div class="row g-3">` 之前添加同样的代码块。

### 6. 国际化修复（生成语言文件）

#### 6a. 将模型和表单中的中文 msgid 改为英文

**文件：`shop/models.py`** — 将所有 `gettext_lazy` 的 msgid 从中文改为英文：

| 字段 | 原值 | 新值 |
|---|---|---|
| `Category.name_zh.verbose_name` | `"名称(中文)"` | `"Name (Chinese)"` |
| `Category.name_en.verbose_name` | `"名称(英文)"` | `"Name (English)"` |
| `Category.image.verbose_name` | `"分类图片"` | `"Category Image"` |
| `Category.order.verbose_name` | `"排序"` | `"Order"` |
| `Category.is_active.verbose_name` | `"启用"` | `"Active"` |
| `Category.Meta.verbose_name` | `"分类"` | `"Category"` |
| `Category.Meta.verbose_name_plural` | `"分类"` | `"Categories"` |
| `Product.category.verbose_name` | `"分类"` | `"Category"` |
| `Product.name_zh.verbose_name` | `"名称(中文)"` | `"Name (Chinese)"` |
| `Product.name_en.verbose_name` | `"名称(英文)"` | `"Name (English)"` |
| `Product.image.verbose_name` | `"主图"` | `"Main Image"` |
| `Product.specs_zh.verbose_name` | `"规格(中文)"` | `"Specs (Chinese)"` |
| `Product.specs_en.verbose_name` | `"规格(英文)"` | `"Specs (English)"` |
| `Product.desc_zh.verbose_name` | `"描述(中文)"` | `"Description (Chinese)"` |
| `Product.desc_en.verbose_name` | `"描述(英文)"` | `"Description (English)"` |
| `Product.price.verbose_name` | `"价格"` | `"Price"` |
| `Product.stock.verbose_name` | `"库存"` | `"Stock"` |
| `Product.is_featured.verbose_name` | `"精选"` | `"Featured"` |
| `Product.is_active.verbose_name` | `"上架"` | `"Active"` |
| `Product.Meta.verbose_name` | `"产品"` | `"Product"` |
| `Product.Meta.verbose_name_plural` | `"产品"` | `"Products"` |
| `ProductImage.product.verbose_name` | `"产品"` | `"Product"` |
| `ProductImage.image.verbose_name` | `"图片"` | `"Image"` |
| `ProductImage.order.verbose_name` | `"排序"` | `"Order"` |
| `ProductImage.Meta.verbose_name` | `"产品图片"` | `"Product Image"` |
| `ProductImage.Meta.verbose_name_plural` | `"产品图片"` | `"Product Images"` |
| `Customer.name.verbose_name` | `"联系人"` | `"Contact Name"` |
| `Customer.company.verbose_name` | `"公司"` | `"Company"` |
| `Customer.email.verbose_name` | `"邮箱"` | `"Email"` |
| `Customer.phone.verbose_name` | `"电话"` | `"Phone"` |
| `Customer.Meta.verbose_name` | `"客户"` | `"Customer"` |
| `Customer.Meta.verbose_name_plural` | `"客户"` | `"Customers"` |
| `Address.customer.verbose_name` | `"客户"` | `"Customer"` |
| `Address.address_zh.verbose_name` | `"地址(中文)"` | `"Address (Chinese)"` |
| `Address.address_en.verbose_name` | `"地址(英文)"` | `"Address (English)"` |
| `Address.city.verbose_name` | `"城市"` | `"City"` |
| `Address.country.verbose_name` | `"国家"` | `"Country"` |
| `Address.zip_code.verbose_name` | `"邮编"` | `"Zip Code"` |
| `Address.is_default.verbose_name` | `"默认地址"` | `"Default Address"` |
| `Address.Meta.verbose_name` | `"地址"` | `"Address"` |
| `Address.Meta.verbose_name_plural` | `"地址"` | `"Addresses"` |
| `Cart.session_id.verbose_name` | `"会话"` | `"Session"` |
| `CartItem.cart.verbose_name` | `"购物车"` | `"Cart"` |
| `CartItem.quantity.verbose_name` | `"数量"` | `"Quantity"` |
| `Order.customer.verbose_name` | `"客户"` | `"Customer"` |
| `Order.customer_name.verbose_name` | `"联系人"` | `"Contact Name"` |
| `Order.customer_email.verbose_name` | `"邮箱"` | `"Email"` |
| `Order.customer_phone.verbose_name` | `"电话"` | `"Phone"` |
| `Order.shipping_address.verbose_name` | `"收货地址"` | `"Shipping Address"` |
| `Order.status.verbose_name` | `"状态"` | `"Status"` |
| `Order.total.verbose_name` | `"总额"` | `"Total"` |
| `Order.Meta.verbose_name` | `"订单"` | `"Order"` |
| `Order.Meta.verbose_name_plural` | `"订单"` | `"Orders"` |
| `OrderItem.order.verbose_name` | `"订单"` | `"Order"` |
| `OrderItem.product_name.verbose_name` | `"产品名"` | `"Product Name"` |
| `OrderItem.product_price.verbose_name` | `"单价"` | `"Unit Price"` |
| `OrderItem.quantity.verbose_name` | `"数量"` | `"Quantity"` |
| `OrderItem.subtotal.verbose_name` | `"小计"` | `"Subtotal"` |
| `OrderItem.Meta.verbose_name` | `"订单项"` | `"Order Item"` |
| `OrderItem.Meta.verbose_name_plural` | `"订单项"` | `"Order Items"` |
| `ContactInquiry.name.verbose_name` | `"姓名"` | `"Name"` |
| `ContactInquiry.company.verbose_name` | `"公司"` | `"Company"` |
| `ContactInquiry.email.verbose_name` | `"邮箱"` | `"Email"` |
| `ContactInquiry.phone.verbose_name` | `"电话"` | `"Phone"` |
| `ContactInquiry.product.verbose_name` | `"产品"` | `"Product"` |
| `ContactInquiry.message.verbose_name` | `"留言"` | `"Message"` |
| `ContactInquiry.Meta.verbose_name` | `"询盘"` | `"Inquiry"` |
| `ContactInquiry.Meta.verbose_name_plural` | `"询盘"` | `"Inquiries"` |

**Order STATUS_CHOICES label 修改：**

| 当前值 | 新值 |
|---|---|
| `_("待付款")` | `_("Pending")` |
| `_("已付款")` | `_("Paid")` |
| `_("处理中")` | `_("Processing")` |
| `_("已发货")` | `_("Shipped")` |
| `_("已签收")` | `_("Delivered")` |
| `_("已取消")` | `_("Cancelled")` |

**文件：`shop/forms.py`** — 将 `CheckoutForm` 和 `ContactForm` 各字段的 `label=` 从中文改为英文，对照同上。

#### 6b. 生成 .po 文件

在项目根目录执行：
```
django-admin makemessages -l zh-hans
```

#### 6c. 编辑 .po 文件

打开 `locale/zh_hans/LC_MESSAGES/django.po`，对每个英文 `msgid` 填入中文 `msgstr`。大致翻译对照：
- "Home" → "首页"
- "Products" → "产品"
- "About Us" → "关于我们"
- "Contact" → "联系我们"
- "Shopping Cart" → "购物车"
- "Checkout" → "结算"
- "Search" → "搜索"
- "Categories" → "分类"
- "Category" → "分类"
- "Price" → "价格"
- "Quantity" → "数量"
- "Subtotal" → "小计"
- "Total" → "合计"
- （注意：模型中的 verbose_name 也要翻译，如 "Name (Chinese)" → "名称(中文)"，以此类推）

#### 6d. 编译语言文件

```
django-admin compilemessages
```

### 验证

```bash
python manage.py check --deploy
python manage.py test
```

全部无报错即修复完成。
