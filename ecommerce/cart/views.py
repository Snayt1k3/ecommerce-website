from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView
from profile_user.models import SellerStatistics
from shop.models import Cart, Product


# Create your views here.


class CartView(ListView):
    template_name = 'cart/cart.html'
    context_object_name = 'user_cart'

    def get_queryset(self):
        items = Cart.objects.filter(user=self.request.user).order_by('-quantity')
        return items

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        total = 0
        for item in self.object_list:
            total += item.sub_total()
        context['total'] = total
        return context


def add_to_cart(request):
    """Добавление Товара В Корзину"""
    if request.method == 'POST':
        if request.user.is_authenticated:
            product = Product.objects.get(id=request.POST.get('product_id'))
            if product:
                if product.stock > 0:
                    if Cart.objects.filter(product=product, user=request.user.id):
                        return JsonResponse({'status': 'Product Already added'})
                    else:
                        # Для статистики (продавца)
                        if product.seller:
                            seller_stat = SellerStatistics.objects.get(product=product)
                            seller_stat.add_cart += 1
                            seller_stat.save()

                        Cart.objects.create(user=request.user, product=product)
                        return JsonResponse({'status': 'Successfully Added'})
                else:
                    return JsonResponse({'status': 'Product out of stock'})
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
            if product.seller:
                seller_stat = SellerStatistics.objects.get(product=product)
                seller_stat.remove_cart += 1
                seller_stat.save()
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

        # Для статистики (продавца)
        if product.seller:
            seller_stat = SellerStatistics.objects.get(product=product)
            seller_stat.remove_cart += 1
            seller_stat.save()

        cart_item = Cart.objects.get(product=product, user=request.user.id)
        cart_item.delete()
        return JsonResponse({'status': 'Successfully Deleted'})
    else:
        return redirect('/')
