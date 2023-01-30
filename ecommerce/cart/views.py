from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from profile_user.models import SellerStatistics
from shop.models import Product, PromoCode

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


@require_POST
def activate_view(request):
    if request.user.is_authenticated:
        if PromoCode.objects.filter(name=request.POST.get('promo')):
            promo = PromoCode.objects.get(name=request.POST.get('promo'))
            cart = Cart(request)

            if cart.get_total_price() > promo.from_the_price:
                request.session['promo'] = {
                    'name': promo.name,
                    'is_percent': promo.is_percent,
                    'amount_of_discount': promo.amount_of_discount
                }

                return JsonResponse({'status': 'Промокод Активирован', 'error': False,
                                     'promo': {
                                         'is_percent': promo.is_percent,
                                         'amount_of_discount': promo.amount_of_discount,
                                     }})

            else:
                return JsonResponse({'status': f'Этот Промокод действует от цены {promo.from_the_price}руб',
                                     'error': True})
        else:
            return JsonResponse({'status': 'Такого Промокода не существует', 'error': True})
    else:
        return JsonResponse({'status': 'Вам нужно авторизоваться', 'error': True})
