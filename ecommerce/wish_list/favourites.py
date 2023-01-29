from shop.models import Product


class Favourites(object):
    def __init__(self, request):
        self.request = request

        self.fav = self.request.session.get('fav')
        if not self.fav:
            self.request.session['fav'] = []
            self.fav = self.request.session.get('fav')

        self.save()

    def add(self, product):
        product_id = str(product.id)

        if product_id not in self.fav:
            self.fav.append(product_id)

        self.save()

    def delete(self, product):
        product_id = str(product.id)
        if product_id in self.fav:
            self.fav.remove(product_id)

        self.save()

    def __iter__(self):
        # получение объектов product и добавление их в избранное
        products = Product.objects.filter(id__in=self.fav)
        for product in products:
            yield product

    def __len__(self):
        return len(self.fav)

    def get_total_price(self):
        """Вычисление все стоимости Избранного"""
        total = 0
        products = Product.objects.filter(id__in=self.fav)
        for product in products:
            total += product.price
        return total

    def save(self):
        # Обновление сессии Избранного
        self.request.session['fav'] = self.fav
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.request.session.modified = True
