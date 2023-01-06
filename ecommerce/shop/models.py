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
    name = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    characteristics = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    img = models.URLField()
    slug = models.SlugField(max_length=1000)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def save(self, *args, **kwargs):
        self.slug = self.slugify_rus(self.name)
        super(Product, self).save(*args, **kwargs)

    def slugify_rus(self, s):
        """
        Overriding django slugify that allows to use russian words as well.
        """
        return slugify(''.join(alphabet.get(w, w) for w in s.lower()))

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('one_pr', args=[self.slug])
