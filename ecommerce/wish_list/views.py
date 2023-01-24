from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView
from profile_user.models import SellerStatistics
from shop.models import Product, WishList


# Create your views here.
def add_to_wish_list(request):
    """Добавление в Избранное"""
    if request.method == 'POST':
        if request.user.is_authenticated:
            product = Product.objects.get(id=request.POST.get('product_id'))
            if WishList.objects.filter(
                    product=request.POST.get('product_id'), user=request.user.id):
                return JsonResponse(
                    {'status': 'Product Already added'})
            else:
                if product.seller:
                    seller_stat = SellerStatistics.objects.get(product=product)
                    seller_stat.add_wish_list += 1
                    seller_stat.save()
                WishList.objects.create(user=request.user, product=product)
                return JsonResponse({'status': 'Successfully Added'})
        else:
            return JsonResponse({'status': 'Login to continue'})

    return redirect('/')


def delete_from_wish_list(request):
    """Удаление из Избранного"""
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST.get('product_id'))
        if product:
            WishList.objects.get(product=product).delete()
            if product.seller:
                seller_stat = SellerStatistics.objects.get(product=product)
                seller_stat.remove_wish_list += 1
                seller_stat.save()
            return JsonResponse({'status': 'Successfully deleted'})
        else:
            return JsonResponse({'status': 'Product unavailable'})
    else:
        return redirect('/')


class WishListView(ListView):
    template_name = 'shop/wishlist.html'
    context_object_name = 'wish_products'

    def get_queryset(self):
        return WishList.objects.filter(user=self.request.user)
