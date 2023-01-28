from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from profile_user.models import SellerStatistics
from shop.models import Product

from .cart import Cart


# Create your views here.
def cart_detail(request):
    return render(request, 'cart/cart.html', {'cart': Cart(request)})


@require_POST
def add_to_cart(request):
    """Добавление Товара В Корзину"""
    cart = Cart(request)
    product = Product.objects.get(id=request.POST.get('product_id'))
    if product.stock > 0:
        cart.add(product)

        if product.seller:
            seller_stat = SellerStatistics.objects.get(product=product)
            seller_stat.add_cart += 1
            seller_stat.save()

        return JsonResponse({'status': 'Товар Обновлен'})
    else:
        return JsonResponse({'status': 'Продукт Закончился'})


@require_POST
def minus_quantity(request):
    """Уменьшение Кол-ва Товара в корзине"""
    cart = Cart(request)
    product = Product.objects.get(id=request.POST.get('product_id'))
    cart.minus(product)
    return JsonResponse({'status': 'Товар Обновлен'})


@require_POST
def delete_from_cart(request):
    """Удаление Товара Из Корзины"""
    cart = Cart(request)
    product = Product.objects.get(id=request.POST.get('product_id'))

    # Для статистики (продавца)
    if product.seller:
        seller_stat = SellerStatistics.objects.get(product=product)
        seller_stat.remove_cart += 1
        seller_stat.save()

    cart.delete(product)

    return JsonResponse({'status': 'Успешно Удален'})
