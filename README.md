# django-trade-site

中英双语 B2B 外贸独立站 — CNC 精密机械产品展示、购物车、下单、询盘系统。

**https://github.com/heliumgenius/django-trade-site**

---

## 快速开始

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data      # 导入产品数据
python manage.py runserver
# → http://localhost:8000/en/
```

管理后台：`http://localhost:8000/admin/`（需创建超级用户 `python manage.py createsuperuser`）

## 技术栈

| 层 | 技术 |
|-------|------|
| 后端 | Django 6.0 |
| 数据库 | SQLite（可换 PostgreSQL） |
| 前端 | Bootstrap 5.3 + Bootstrap Icons + 自定义 CSS/JS |
| 国际化 | Django i18n（中文/English URL 前缀） |
| 测试 | Django TestCase — 33 条 |
| 部署 | Gunicorn + PythonAnywhere（可选） |

## 项目结构

```
├── config/
│   ├── settings.py            # Django 配置（i18n、静态文件、数据库）
│   ├── urls.py                # 根路由，i18n_patterns 包裹
│   └── wsgi.py                # WSGI 入口
├── shop/                      # 主应用
│   ├── models.py              # 10 个模型（分类/产品/购物车/订单/询盘…）
│   ├── views.py               # 13 个类视图
│   ├── forms.py               # 结账表单 + 联系表单
│   ├── cart.py                # session 购物车逻辑
│   ├── checkout.py            # 事务原子下单
│   ├── admin.py               # Django 管理后台注册
│   ├── context_processors.py  # 全局上下文（分类、购物车数量）
│   └── management/commands/
│       └── seed_data.py       # 从 YAML 导入产品到数据库
├── data/
│   └── products.yaml          # 产品种子数据
├── locale/
│   └── zh_Hans/LC_MESSAGES/   # 中文翻译文件（.po/.mo）
├── templates/
│   ├── base.html              # 导航栏 + 页脚 + 语言切换
│   ├── index.html             # 首页（hero + 分类 + 精选产品 + CTA）
│   └── shop/
│       ├── product_list.html      # 产品列表（分类筛选 + 搜索）
│       ├── product_detail.html    # 产品详情（规格/描述/相关产品）
│       ├── cart.html              # 购物车
│       ├── checkout.html          # 结账
│       ├── order_success.html     # 下单成功
│       ├── order_list.html        # 订单查询
│       ├── order_detail.html      # 订单详情
│       ├── contact.html           # 联系询盘
│       └── about.html             # 关于我们
├── static/
│   ├── css/style.css          # Apple 风格设计系统
│   └── js/main.js             # 图片回退、导航高亮、平滑滚动
└── docs/
    ├── fix-plan.md            # 修复计划
    └── specs/                 # UI/部署规格文档
```

## 路由

| URL | 页面 |
|-----|------|
| `/` | 重定向 → `/en/` |
| `<lang>/` | 首页 |
| `<lang>/products/` | 产品列表（筛选 + 搜索 + 分页） |
| `<lang>/products/<slug>/` | 产品详情（规格/描述/加购/相关产品） |
| `<lang>/cart/` | 购物车 |
| `<lang>/cart/add/<id>/` | 加入购物车（POST） |
| `<lang>/cart/remove/<id>/` | 移除（POST） |
| `<lang>/cart/update/<id>/` | 更新数量（POST） |
| `<lang>/checkout/` | 结账 |
| `<lang>/checkout/success/<id>/` | 下单成功 |
| `<lang>/orders/` | 按邮箱查订单 |
| `<lang>/orders/<pk>/` | 订单详情 |
| `<lang>/about/` | 关于我们 |
| `<lang>/contact/` | 联系询盘 |
| `/admin/` | Django Admin |

## 数据模型

| 模型 | 说明 |
|------|------|
| Category | 产品分类（中英文名、slug、排序） |
| Product | 产品（中英文名、规格、描述、价格、库存） |
| ProductImage | 产品多图 |
| Customer | 客户（邮箱唯一） |
| Address | 客户地址 |
| Cart | 购物车（session 绑定） |
| CartItem | 购物车项（关联产品 + 数量） |
| Order | 订单（6 状态：待付款→已签收） |
| OrderItem | 订单项（快照产品名/价格/数量/小计） |
| ContactInquiry | 询盘记录 |

## 测试

```bash
python manage.py test       # 33 条测试，全部通过
```

## 环境变量

复制 `.env.example` 为 `.env`：

| 变量 | 说明 |
|----------|---------|
| `SECRET_KEY` | Django 密钥（生产必须换强随机值） |
| `DEBUG` | 调试模式（生产设为 False） |

## 设计风格

Apple 官网风格 — 深色导航 `#161617`、黑色 hero、蓝色强调 `#0071e3`、18px 圆角卡片、药丸形按钮。详见 `docs/specs/`。

## 与 Flask 版对比

本项目兄弟项目：[flask-trade-site](https://github.com/heliumgenius/flask-trade-site)

| 维度 | Flask 版 | Django 版（本项目） |
|--------|-----------|----------|
| 功能 | 产品展示 + 询盘 | + 购物车 + 下单 + 订单追踪 + Admin |
| 数据 | YAML + SQLite | Django ORM + SQLite |
| 管理后台 | 无 | Django Admin |
| 测试 | 27 条 pytest | 33 条 Django TestCase |
| 定位 | 轻量展示 | 功能完整，偏生产 |

## 已知限制

- 图片为占位图（目录空）
- 支付为模拟（演示站，不产生实际交易）
- PythonAnywhere 免费版有出站网络限制（邮箱需第三方 API）
