from abc import ABC, abstractmethod

class Observable:
    def __init__(self):
        self._subscribers = []

    def subscribe(self, sub):
        if sub not in self._subscribers:
            self._subscribers.append(sub)

    def unsubscribe(self, sub):
        if sub in self._subscribers:
            self._subscribers.remove(sub)

    def _notify(self, event, data):
        for sub in list(self._subscribers):
            sub.update(event, data)

class Product:
    def __init__(self, sku, name, price):
        if price <= 0:
            raise ValueError("Цена должна быть положительной")
        self.sku, self.name, self.price = sku, name, price

class CartItem:
    BULK_QTY, BULK_DISCOUNT = 3, 0.10

    def __init__(self, product, qty):
        self.product, self.qty = product, qty

    @property
    def discount(self):
        return self.BULK_DISCOUNT if self.qty >= self.BULK_QTY else 0.0

    @property
    def subtotal(self):
        return self.product.price * self.qty * (1 - self.discount)

class InventoryService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._stock = {}
            cls._instance._reserved = {}
        return cls._instance

    def add_stock(self, product, qty):
        self._stock[product.sku] = self._stock.get(product.sku, 0) + qty

    def available(self, product):
        return self._stock.get(product.sku, 0) - self._reserved.get(product.sku, 0)

    def update(self, event, data):
        if event == "ITEM_ADDED":
            sku = data["product"].sku
            self._reserved[sku] = self._reserved.get(sku, 0) + data["qty"]
        elif event == "ITEM_REMOVED":
            sku = data["product"].sku
            self._reserved[sku] = self._reserved.get(sku, 0) - data["qty"]
        elif event == "CHECKOUT":
            for product, qty in data["items"]:
                self._stock[product.sku] -= qty
                self._reserved[product.sku] -= qty

    def report(self):
        print("Склад:")
        for sku, qty in self._stock.items():
            print(f"  {sku:<8s} на складе {qty:>3d} | в резерве {self._reserved.get(sku, 0)}")

class NotificationService:
    def update(self, event, data):
        print(f"    [Уведомление] {data['text']}")

class Payment(ABC):
    NAME = ""

    @abstractmethod
    def fee(self, amount):
        pass

    def pay(self, amount):
        total = amount + self.fee(amount)
        return f"{self.NAME}: {amount:,.2f} + комиссия {self.fee(amount):,.2f} = {total:,.2f} сом"

class CardPayment(Payment):
    NAME = "Банковская карта"

    def __init__(self, card_last4="0000"):
        self.card_last4 = card_last4

    def fee(self, amount):
        return 0.0

class CashPayment(Payment):
    NAME = "Наличные"

    def fee(self, amount):
        return 0.0

class QRPayment(Payment):
    NAME = "QR-код"

    def fee(self, amount):
        return amount * 0.005

class InstallmentPayment(Payment):
    NAME = "Рассрочка"

    def __init__(self, months=6):
        if months not in (3, 6, 12):
            raise ValueError("Рассрочка возможна на 3, 6 или 12 месяцев")
        self.months = months

    def fee(self, amount):
        return amount * 0.01 * self.months

    def pay(self, amount):
        base = super().pay(amount)
        monthly = (amount + self.fee(amount)) / self.months
        return f"{base} ({self.months} мес. по {monthly:,.2f})"

class PaymentFactory:
    _registry = {"card": CardPayment, "cash": CashPayment,
                 "qr": QRPayment, "installment": InstallmentPayment}

    @classmethod
    def create(cls, kind, **kwargs):
        creator = cls._registry.get(kind)
        if creator is None:
            raise ValueError(f"Неизвестный способ оплаты: {kind}")
        return creator(**kwargs)

class ShoppingCart(Observable):
    PROMO = {"SALE5": 0.05, "WELCOME10": 0.10}
    BIG_ORDER_LIMIT, BIG_ORDER_DISCOUNT = 50_000, 0.05

    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self._items = {}
        self.subscribe(NotificationService())
        self.subscribe(InventoryService())

    def add(self, product, qty=1):
        if qty <= 0:
            raise ValueError("Количество должно быть положительным")
        if InventoryService().available(product) < qty:
            raise ValueError(f"Недостаточно «{product.name}» на складе "
                             f"(доступно {InventoryService().available(product)})")
        item = self._items.get(product.sku)
        if item:
            item.qty += qty
        else:
            self._items[product.sku] = CartItem(product, qty)
        self._notify("ITEM_ADDED", {"product": product, "qty": qty,
                                    "text": f"{self.owner}: +{qty} × {product.name}"})

    def remove(self, sku, qty=None):
        item = self._items.get(sku)
        if item is None:
            raise ValueError(f"Товара {sku} нет в корзине")
        qty = item.qty if qty is None else min(qty, item.qty)
        item.qty -= qty
        if item.qty == 0:
            del self._items[sku]
        self._notify("ITEM_REMOVED", {"product": item.product, "qty": qty,
                                      "text": f"{self.owner}: −{qty} × {item.product.name}"})

    def subtotal(self):
        return sum(i.subtotal for i in self._items.values())

    def show(self):
        print(f"Корзина {self.owner}:")
        for i in self._items.values():
            d = f" (скидка {i.discount:.0%})" if i.discount else ""
            print(f"  {i.product.name:<18s} {i.product.price:>9,.0f} × {i.qty} = {i.subtotal:>10,.2f}{d}")

    def checkout(self, payment_kind, promo=None, **payment_kwargs):
        if not self._items:
            raise ValueError("Корзина пуста")
        total = self.subtotal()
        lines = [f"Сумма с учётом скидок на позиции: {total:,.2f} сом"]
        if total >= self.BIG_ORDER_LIMIT:
            cut = total * self.BIG_ORDER_DISCOUNT
            total -= cut
            lines.append(f"Скидка за крупный заказ 5 %: −{cut:,.2f}")
        if promo:
            if promo not in self.PROMO:
                raise ValueError(f"Недействительный промокод: {promo}")
            cut = total * self.PROMO[promo]
            total -= cut
            lines.append(f"Промокод {promo} (−{self.PROMO[promo]:.0%}): −{cut:,.2f}")
        payment = PaymentFactory.create(payment_kind, **payment_kwargs)
        items = [(i.product, i.qty) for i in self._items.values()]
        self._notify("CHECKOUT", {"items": items,
                                  "text": f"{self.owner}: заказ оформлен на {total:,.2f} сом"})
        self._items.clear()
        lines.append("Итог к оплате — " + payment.pay(total))
        return "\n".join(lines)

if __name__ == "__main__":
    laptop = Product("NB-01", "Ноутбук", 45_000)
    mouse = Product("MS-02", "Мышь", 800)
    phone = Product("PH-03", "Смартфон", 22_000)
    inv = InventoryService()
    inv.add_stock(laptop, 3)
    inv.add_stock(mouse, 20)
    inv.add_stock(phone, 5)
    inv.report()
    print("\n--- Покупатель 1 ---")
    cart1 = ShoppingCart("Айдар")
    cart1.add(laptop, 1)
    cart1.add(mouse, 4)
    cart1.add(phone)
    cart1.remove("PH-03")
    cart1.show()
    print("\n--- Покупатель 2 пытается взять оставшиеся ноутбуки ---")
    cart2 = ShoppingCart("Бермет")
    cart2.add(laptop, 2)
    for action in (lambda: cart2.add(laptop, 1), lambda: cart2.remove("XX-99"),
                   lambda: cart2.add(mouse, 0)):
        try:
            action()
        except ValueError as e:
            print("  ValueError:", e)
    inv.report()
    print("\n--- Оформление заказа 1 (QR + промокод) ---")
    print(cart1.checkout("qr", promo="SALE5"))
    print("\n--- Оформление заказа 2 (рассрочка) ---")
    cart2.show()
    print(cart2.checkout("installment", months=12))
    print("\n--- Ошибки ---")
    cart3 = ShoppingCart("Нурлан")
    for action in (lambda: cart3.checkout("cash"),
                   lambda: (cart3.add(mouse, 2), cart3.checkout("bitcoin")),
                   lambda: cart3.checkout("card", promo="FAKE"),
                   lambda: cart3.checkout("installment", months=5)):
        try:
            action()
        except ValueError as e:
            print("  ValueError:", e)
    print()
    inv.report()
    print("Один склад:", InventoryService() is InventoryService())