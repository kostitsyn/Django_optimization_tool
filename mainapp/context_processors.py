from basketapp.models import Basket


def get_basket(request):
    basket_items = []

    if request.user.is_authenticated:
        basket_items = Basket.objects.filter(user=request.user)
        # basket_items = Basket.objects.filter(user=request.user).select_related('product')

    return {
        'basket': basket_items
    }