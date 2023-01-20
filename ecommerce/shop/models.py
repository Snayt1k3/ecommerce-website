from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e',
            'ю': 'yu',
            'я': 'ya'}


# Create your models here.


class Category(models.Model):
    """Класс Категории Продукта"""
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ('category_name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        self.slug = self.slugify_rus(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def slugify_rus(self, s):
        """
        Overriding django slugify that allows to use russian words as well.
        """
        return slugify(''.join(alphabet.get(w, w) for w in s.lower()))

    def __str__(self):
        return self.category_name


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    characteristics = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    img = models.URLField()
    slug = models.SlugField(max_length=1000)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def save(self, *args, **kwargs):
        self.slug = self.slugify_rus(self.name)
        super(Product, self).save(*args, **kwargs)

    @staticmethod
    def slugify_rus(s):
        """
        Overriding django slugify that allows to use russian words as well.
        """
        return slugify(''.join(alphabet.get(w, w) for w in s.lower()))

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('one_pr', args=[self.slug])


class Review(models.Model):
    """Отзывы"""
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    rating = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('date',)
        verbose_name = 'review'
        verbose_name_plural = 'reviews'


class ReviewImages(models.Model):
    """Для изображений с отзывов"""
    img = models.ImageField(upload_to='media')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, default='')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'ReviewImages'
        verbose_name_plural = 'ReviewImages'


class WishList(models.Model):
    """Избранное"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'WishList'
        verbose_name_plural = 'WishLists'


class Cart(models.Model):
    """Корзина"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def sub_total(self):
        return self.product.price * self.quantity


class OrdersItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'OrderItem'
        verbose_name_plural = 'OrderItems'


class Orders(models.Model):
    CHOICES = (
        ('assembl', 'В сборке у продавца'),
        ('delivery', 'В доставке'),
        ('received', 'Получен')
    )
    order_items = models.ManyToManyField(OrdersItem)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=CHOICES)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['date']


class PersonalArea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media/avatars', blank=False)
    address = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=100, blank=False)
