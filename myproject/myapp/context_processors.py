from .models import Order

def order_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-order_date')
        return {'order_history': orders}
    return {}