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
    slug = models.SlugField(max_length=100, blank=True)

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
    price = models.FloatField()
    description = models.TextField()
    characteristics = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='products/')
    slug = models.SlugField(max_length=1000, blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

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
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class OrdersItem(models.Model):
    """Для Order, Чтобы хранить какие-то смежные данные"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Order_Item'
        verbose_name_plural = 'Order_Items'


class Orders(models.Model):
    """Модель Заказа"""
    CHOICES = (
        ('В сборке у продавца', 'assembl'),
        ('В доставке', 'delivery'),
        ('Получен', 'received')
    )
    order_items = models.ManyToManyField(OrdersItem)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=CHOICES, blank=False, default='В сборке у продавца')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['date']


class PromoCode(models.Model):
    """Промокоды"""
    # Сам промокод
    name = models.CharField(max_length=10)

    # Скидка процентная или нет
    is_percent = models.BooleanField(default=False)

    # От какой цены скидка
    from_the_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Размер Скидки
    amount_of_discount = models.IntegerField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PersonalArea(models.Model):
    # Информация О пользователе
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email_confirm = models.BooleanField(default=False)
    slug = models.SlugField(blank=True)

    # Для продавцов
    is_seller = models.BooleanField(default=False)
    your_products = models.ManyToManyField(Product, blank=True)
    avg_rating = models.FloatField(default=0.0)

    # Заработок и траты
    all_spent_money = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    all_earned_money = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Personal_Area'
        verbose_name_plural = 'Personal_Areas'

    @staticmethod
    def slugify_rus(s):
        """
        Overriding django slugify that allows to use russian words as well.
        """
        return slugify(''.join(alphabet.get(w, w) for w in s.lower()))

    def save(self, *args, **kwargs):
        self.slug = self.slugify_rus(self.user.username)
        super(PersonalArea, self).save(*args, **kwargs)


class ReviewSeller(models.Model):
    """Отзыв На Продавца"""
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    feedback = models.TextField()
    rating = models.CharField(choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')), max_length=1)
    date = models.DateField(auto_now_add=True, null=True)
