from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from profile_user.models import SellerStatistics
from shop.models import Product
from django.shortcuts import render
from .favourites import Favourites


# Create your views here.
@require_POST
def add_to_wish_list(request):
    """Добавление в Избранное"""
    fav = Favourites(request)
    product = Product.objects.get(id=request.POST.get('product_id'))

    if product.id in request.session.get('fav'):
        return JsonResponse({'status', 'Товар уже в избранном'})

    fav.add(product)

    if product.seller:
        seller_stat = SellerStatistics.objects.get(product=product)
        seller_stat.add_wish_list += 1
        seller_stat.save()

    return JsonResponse({'status': 'Товар добавлен в избранное'})


@require_POST
def delete_from_wish_list(request):
    """Удаление из Избранного"""

    fav = Favourites(request)
    product = Product.objects.get(id=request.POST.get('product_id'))

    if str(product.id) not in request.session.get('fav'):
        return JsonResponse({'status': 'Товар Уже Удален'})

    fav.delete(product)

    if product.seller:
        seller_stat = SellerStatistics.objects.get(product=product)
        seller_stat.remove_wish_list += 1
        seller_stat.save()

    return JsonResponse({'status': 'Успешно удален'})


def favourites_view(request):
    return render(request, 'favourites/favourites2.html', {'favourites': Favourites(request)})
