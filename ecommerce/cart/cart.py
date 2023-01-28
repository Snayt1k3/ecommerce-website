from shop.models import Product


class Cart(object):
    def __init__(self, request):
        """Инициализация Корзины"""
        self.request = request
        self.cart = request.session.get('cart')
        if not self.cart:
            self.request.session['cart'] = {}
            self.cart = request.session.get('cart')

    def add(self, product):
        """
        Добавление товара в корзину, если он уже есть
        прибавляем к количеству
        """
        id_product = str(product.id)
        if id_product not in self.cart:
            self.cart[id_product] = {
                'quantity': 1,
                'price': int(product.price)
            }
        else:
            self.cart[id_product]['quantity'] += 1
        self.save()

    def minus(self, product):
        """Убавляем количество товара в корзине"""
        id_product = str(product.id)

        if id_product in self.cart and self.cart[id_product]['quantity'] > 1:
            self.cart[id_product]['quantity'] -= 1

        else:
            self.delete(product)

        self.save()

    def delete(self, product):
        """Удаление товара из корзины"""
        id_product = str(product.id)
        if id_product in self.cart:
            del self.cart[id_product]

        self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(int(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def save(self):
        # Обновление сессии cart
        self.request.session['cart'] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.request.session.modified = True
