from . views import *
from cart.views import *

def cat(request):
    cata = cate.objects.all()
    return {'c':cata}

def count(request, count=0):
    user = request.user

    if user.is_authenticated:
        ct = cartlist.objects.filter(user=user)
    else:
        cart_id = request.session.get(
            'cart_id')  # here this else case is not working because of the decorator(login)
        ct = cartlist.objects.filter(cart_id=cart_id)
    # -------------------------------------------------------------------------
    ct_items = items.objects.filter(cart__in=ct, active=True)
    for i in ct_items:
        # tot += (i.prod.price * i.quan)
        count += i.quan


    return {'cn': count}

