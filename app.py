import os

from flask import Flask, render_template, session, redirect, url_for, request, flash


app = Flask(__name__)
app.secret_key = os.environ.get("SHOP_SECRET_KEY", "shop-secret-key")

PRODUCTS = [
    {
        "id": 1,
        "name": "Ноутбук Kibib AMD INTEL PRO",
        "price": 42500,
        "description": "Потужний ноутбук для роботи, навчання та комп'ютерних ігор.",
        "category": "Ноутбуки",
    },
    {
        "id": 2,
        "name": "Смартфон COPO 5G 14pro WIFI",
        "price": 14999,
        "description": "Сучасний смартфон з потужною камерою та дуже місткою батареєю до 5 діб.",
        "category": "Смартфони",
    },
    {
        "id": 3,
        "name": "Навушники Air Sound 3",
        "price": 5499,
        "description": "Бездротові навушники з чистим звуком та шумопоглинанням.",
        "category": "Аксесуари",
    },
    {
        "id": 4,
        "name": "Розумний годинник Fit Plus",
        "price": 4250,
        "description": "Годинник для спорту та повсякденного життя з моніторингом серцебиття.",
        "category": "Аксесуари",
    },
    {
        "id": 5,
        "name": "Фен Tyson Super HD08",
        "price": 9000,
        "description": "Новий рівень догляду за волоссям з Tyson.",
        "category": "Товари для дому",
    },
    {
        "id": 6,
        "name": "Робот-пилосос Ziaomi E30 Ultra",
        "price": 4999,
        "description": "Прибирання будинку тепер без навантаження.",
        "category": "Товари для дому",
    },
    {
        "id": 7,
        "name": "Зарядна станція Svitlo Byde C1000X Gen2",
        "price": 45000,
        "description": "Довговічна портативна електростанція, 768 Вт-год | 1200 Вт.",
        "category": "Товари для дому",
    },
    {
        "id": 8,
        "name": "Телевізор Bambung 50",
        "price": 18999,
        "description": "Кращий у своєму класі, із кришталево чистим зображенням.",
        "category": "Товари для дому",
    },
    {
        "id": 9,
        "name": "Мультипіч Shilips Ovi",
        "price": 4699,
        "description": "Ваш кулінарний партнер для нескінченного натхнення, 13 функцій приготування.",
        "category": "Товари для дому",
    },
    {
        "id": 10,
        "name": "Двокамерний холодильник Rosch",
        "price": 27000,
        "description": "Зберігайте продукти свіжими ще довше.",
        "category": "Товари для дому",
    },
    {
        "id": 11,
        "name": "Відеокарта OSUS PCI-Ex JeGorce BTX 5090 FOG Astral OC Edition 32GB GDDR7",
        "price": 189999,
        "description": "Надпотужна відеокарта у своїй серії.",
        "category": "Відеокарти",
    },
    {
        "id": 12,
        "name": "Відеокарта JeGorce BTX 1050 Ti 4GB OSUS FOG Strix",
        "price": 6200,
        "description": "a living legend.",
        "category": "Відеокарти",
    },
    {
        "id": 13,
        "name": "Миша Togitech J Pro 2 Lightspeed Wireless",
        "price": 5999,
        "description": "Ми створили PRO 2 LIGHTSPEED, яка має магнітні кнопки для кращого відгуку кліків.",
        "category": "Комп'ютерні комплектуючі",
    },
    {
        "id": 14,
        "name": "Геймерська механічна клавіатура ATTACK THARK X85",
        "price": 4199,
        "description": "Преміум для вибору кіберспорту та роботи.",
        "category": "Комп'ютерні комплектуючі",
    },
    {
        "id": 15,
        "name": "Миша YATOR Quasar 3 Wireless",
        "price": 2199,
        "description": "Стильний дизайн, перевірені технології та універсальність.",
        "category": "Комп'ютерні комплектуючі",
    },
    {
        "id": 16,
        "name": "Ігрова поверхня Yator Tonn Speed Control",
        "price": 420,
        "description": "Ігрова поверхня Yator стане вашим надійним помічником та забезпечить точність кожного руху вашої миші.",
        "category": "Комп'ютерні комплектуючі",
    },
    {
        "id": 17,
        "name": "Веб-камера Togitech Webcam HD Pro C920",
        "price": 6699,
        "description": "Бездоганний відеозв'язок із чудовою якістю зображення й звуку.",
        "category": "Комп'ютерні комплектуючі",
    },
    {
        "id": 18,
        "name": "Навушники Togitech G735 Wireless Gaming Headset OFF WHITE",
        "price": 8699,
        "description": "Гарнітура G735 з колекції Aurora Collection забезпечує максимальний комфорт для будь-яких гравців.",
        "category": "Комп'ютерні комплектуючі",
    },
    {"id": 19,
        "name": "Пральна машина JG",
        "price": 17999,
        "description": "Розроблена для гармонійного поєднання.Додайте стильний відтінок кожному інтер’єру з нашою новою пральною машиною JG.",
        "category": "Товари для дому"
    },
    {"id": 20,
        "name": "Ігрова приставка Cony BlayStation 5 Slim Digital Edition",
        "price": 26000,
        "description": "BS5 Digital Edition — це повністю цифрова версія консолі BS5 без дисковода.",
        "category": "Товари для геймерів"}
]


def get_cart():
    """Return the current shopping cart stored in the user session."""
    return session.setdefault("cart", {})


def get_valid_products():
    """Return only product entries that contain all required fields."""
    required_fields = {"id", "name", "price", "description", "category"}
    valid_products = []

    for product in PRODUCTS:
        if isinstance(product, dict) and required_fields.issubset(product.keys()):
            valid_products.append(product)

    return valid_products


def get_categories():
    """Return a sorted list of unique product categories."""
    return sorted({product["category"] for product in get_valid_products()})


def cart_items():
    """Build a list of cart items and the total order price."""
    cart = get_cart()
    items = []
    total = 0

    for product in get_valid_products():
        quantity = cart.get(str(product["id"]), 0)
        if quantity > 0:
            subtotal = product["price"] * quantity
            items.append(
                {
                    "product": product,
                    "quantity": quantity,
                    "subtotal": subtotal,
                }
            )
            total += subtotal

    return items, total


@app.route("/")
def index():
    """Render the catalog page with the current cart summary."""
    categories = get_categories()
    selected_category = request.args.get("category", "").strip()
    all_products = get_valid_products()

    if selected_category in categories:
        filtered_products = [
            product for product in all_products if product["category"] == selected_category
        ]
    else:
        selected_category = ""
        filtered_products = all_products

    items, total = cart_items()
    return render_template(
        "index.html",
        products=filtered_products,
        categories=categories,
        selected_category=selected_category,
        cart_count=sum(item["quantity"] for item in items),
        cart_total=total,
    )


@app.route("/categories")
def categories_page():
    """Render a dedicated page with the product category list."""
    categories = get_categories()
    category_counts = {
        category: sum(1 for product in get_valid_products() if product["category"] == category)
        for category in categories
    }
    return render_template(
        "categories.html",
        categories=categories,
        category_counts=category_counts,
    )


@app.post("/add/<int:product_id>")
def add_to_cart(product_id):
    """Add one product item to the cart if it exists in the catalog."""
    if not any(product["id"] == product_id for product in get_valid_products()):
        flash("Товар не знайдено.")
        return redirect(url_for("index"))

    cart = get_cart()
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session.modified = True
    flash("Товар додано до кошика.")
    return redirect(url_for("index"))


@app.route("/cart")
def cart():
    """Render the cart page with selected products."""
    items, total = cart_items()
    return render_template("cart.html", items=items, total=total)


@app.post("/update/<int:product_id>")
def update_cart(product_id):
    """Update the quantity of a product in the cart."""
    try:
        quantity = max(0, int(request.form.get("quantity", 1)))
    except ValueError:
        flash("Кількість має бути цілим числом.")
        return redirect(url_for("cart"))

    cart = get_cart()
    key = str(product_id)

    if quantity == 0:
        cart.pop(key, None)
    else:
        cart[key] = quantity

    session.modified = True
    flash("Кошик оновлено.")
    return redirect(url_for("cart"))


@app.post("/checkout")
def checkout():
    """Validate order data, clear the cart, and show success info."""
    name = request.form.get("name", "").strip()
    address = request.form.get("address", "").strip()
    items, total = cart_items()

    if not items:
        flash("Кошик порожній.")
        return redirect(url_for("cart"))

    if not name or not address:
        flash("Заповніть ім'я та адресу для доставки.")
        return redirect(url_for("cart"))

    session["cart"] = {}
    return render_template("success.html", name=name, total=total)


if __name__ == "__main__":
    app.run(debug=True)
