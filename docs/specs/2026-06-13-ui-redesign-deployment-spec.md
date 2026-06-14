# UI Redesign + Deployment Spec

## 项目背景

Django 6.0 外贸独立站（精密机械 B2B），当前使用 Bootstrap 5 通用样式。需要重新设计为 Apple 官网质感，并部署到 PythonAnywhere 免费版。

## 视觉方向

| 维度 | 规格 |
|---|---|
| 风格参考 | Apple 官网 |
| 配色 | `#161617`（深色导航/页脚）、`#000`（hero 背景）、`#f5f5f7`（浅灰段）、`#1d1d1f`（正文）、`#86868b`（次要文字）、`#0071e3`（蓝色按钮/链接） |
| 字体 | `-apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif` |
| 按钮 | Pill 样式：`border-radius: 980px; padding: 12px 28px` |
| 卡片 | 圆角 `14px` / `18px`，白底或浅灰底 |
| 导航栏 | 深色 52px 细高条，fix 顶部 |
| 页脚 | 深色 `#161617`，三栏网格 |

## 文件改动清单

### 1. `static/css/style.css` — 重写全部样式

- 重写 `:root` 变量（配色、圆角、阴影）
- 按钮：`.btn-accent` 改蓝色 pill，`.btn-outline-primary` 改灰边 pill
- 卡片：`.product-card` / `.category-card` 改圆角白底
- hero：`.hero` 黑色背景，大标题 56px
- page-header：`.page-header` 深色背景
- 导航栏：`.navbar` 深色 52px
- 页脚：`.footer` 深色网格
- 保留 Bootstrap 栅格系统

### 2. `templates/base.html` — 全局布局

- 导航栏改 Apple 风格深色细高条
- 页脚改深色三栏网格
- 保证 `{% load static %}` 和 CSS 链接正确

### 3. `templates/index.html` — 首页

- hero：黑色全幅，56px 大标题、22px 副标题、两个 pill 按钮（蓝色/白边）
- 灰色占位区域（模拟机器大图，420px 高）
- 分类展示：3 列圆角卡片网格
- 精选产品：4 列圆角卡片，产品图+名称+价格
- CTA：浅灰段，获取报价 pill 按钮

### 4. `templates/shop/product_list.html` — 产品列表

- 深色 page-header
- 左侧边栏：分类 pill 列表 + 搜索框
- 右侧：产品 4 列卡片网格

### 5. `templates/shop/product_detail.html` — 产品详情

- 左图右文
- 分类 badge、大标题、价格
- 数量选择 + 蓝色 pill Add to Cart
- 库存显示
- 底部相关产品 4 列网格

### 6. `templates/shop/cart.html` — 购物车

- 简洁表格：产品图+名称、数量控制、小计、删除
- 底部两个 pill 按钮
- 空车居中提示

### 7. `templates/shop/checkout.html` — 结账

- 左表单右摘要布局
- 蓝色 pill 提交按钮
- form errors 已有

### 8. `templates/shop/contact.html` — 联系

- 统一 Apple 配色
- form errors 已有

### 9. 其他页面

- `about.html`、`order_success.html`、`order_list.html`、`order_detail.html`：统一 Apple 配色和排版

## UI 实现注意事项

- 保留 Bootstrap 栅格（`container`、`row`、`col-*`）用于响应式
- 仅覆盖 CSS 视觉样式，不改变 HTML 结构
- 使用 `{% static 'css/style.css' %}` 确保新 CSS 加载

## 已知遗留 Bug（本次修复）

- `shop/models.py` 三处 `_("分类")` → `_("Category")` / `_("Categories")`（已完成）

## 部署（PythonAnywhere 免费版）

### 环境要求

- Python 3.10+
- Django 6.0.6
- gettext（用于编译翻译文件）

### 步骤

1. 注册 PythonAnywhere 免费账号
2. 进入 Bash 终端
3. 从 GitHub clone 仓库：
   ```
   git clone <仓库URL>
   cd <项目目录>
   ```
4. 创建 virtualenv：
   ```
   mkvirtualenv --python=python3.10 django-trade
   ```
5. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
6. 修改 `config/settings.py`：
   - `DEBUG = False`
   - `ALLOWED_HOSTS = ['<username>.pythonanywhere.com']`
   - 确保 `SECRET_KEY` 已设置
7. 编译翻译文件：
   ```
   django-admin compilemessages
   ```
8. 迁移数据库：
   ```
   python manage.py migrate
   ```
9. 收集静态文件：
   ```
   python manage.py collectstatic
   ```
10. 配置 Web 面板：
    - WSGI 配置文件指向 `config.wsgi.application`
    - Static files URL = `/static/`
    - Static files directory = `/home/<username>/<项目目录>/staticfiles`

## 验证

部署后手动验收流程：
- [ ] 首页展示正常
- [ ] 产品列表/详情浏览正常
- [ ] 添加购物车/更新数量/删除正常
- [ ] 结账下单成功
- [ ] 订单查询正常
- [ ] 联系表单提交正常
- [ ] 中英文切换正常
- [ ] 移动端响应式正常
