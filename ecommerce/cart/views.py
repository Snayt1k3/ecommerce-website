from django.http import JsonResponse
from django.shortcuts import render, redirect

from shop.models import Cart, Product


# Create your views here.

def cart(request):
    """Корзина"""
    user_cart = Cart.objects.filter(user=request.user.id)
    total = 0
    for item in user_cart:
        total += item.sub_total()

    return render(request, 'cart/cart.html', context={
        'user_cart': user_cart,
        'total': total,
    })


def add_to_cart(request):
    """Добавление Товара В Корзину"""
    if request.method == 'POST':
        if request.user.is_authenticated:
            product = Product.objects.get(id=request.POST.get('product_id'))
            if product:
                if Cart.objects.filter(product=product, user=request.user.id):
                    return JsonResponse({'status': 'Product Already added'})
                else:
                    Cart.objects.create(user=request.user, product=product)
                    return JsonResponse({'status': 'Successfully Added'})
            else:
                return JsonResponse({'status': 'Product unavailable'})
        else:
            return JsonResponse({'status': 'Login to continue'})
    else:
        return redirect('/')


def minus_quantity(request):
    """Уменьшение Кол-ва Товара в корзине"""
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST.get('product_id'))
        cart_item = Cart.objects.get(product=product, user=request.user.id)
        if cart_item.quantity == 1:
            cart_item.delete()
            return JsonResponse({'status': 'Successfully Deleted from cart'})
        else:
            cart_item.quantity -= 1
            cart_item.save()
            return JsonResponse({'status': 'Quantity Updated'})
    else:
        return redirect('/')


def plus_quantity(request):
    """Увеличение Кол-ва Товара в корзине"""
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST.get('product_id'))
        cart_item = Cart.objects.get(product=product, user=request.user.id)
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            return JsonResponse({'status': 'Quantity Updated'})
        else:
            return JsonResponse({'status': f'Product stock - {product.stock}'})
    else:
        return redirect('/')


def delete_from_cart(request):
    """Удаление Товара Из Корзины"""
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST.get('product_id'))
        cart_item = Cart.objects.get(product=product, user=request.user.id)
        cart_item.delete()
        return JsonResponse({'status': 'Successfully Deleted'})
    else:
        return redirect('/')
