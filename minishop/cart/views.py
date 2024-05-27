from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from home.models import product
from django.core.exceptions import ObjectDoesNotExist

def c_id(request):
    ct_id = request.session.session_key
    if not ct_id:
        ct_id = request.session.create()
    return ct_id

@login_required(login_url='login')
def add_cart(request, product_id):
    prod = get_object_or_404(product, id=product_id)
    user = request.user

    try:
        ct = cartlist.objects.get(user=user)
    except cartlist.DoesNotExist:
        ct = cartlist.objects.create(cart_id=c_id(request), user=user)
        ct.save()

    try:
        c_items = items.objects.get(prod=prod, cart=ct)
        if c_items.quan < c_items.prod.stock:
            c_items.quan += 1
            prod.stock -= 1
            prod.save()
        c_items.save()
    except items.DoesNotExist:
        c_items = items.objects.create(prod=prod, quan=1, cart=ct)
        prod.stock -= 1
        prod.save()
        c_items.save()

    return redirect('cartDetails')

@login_required(login_url='login')
def min_cart(request, product_id):
    user = request.user
    try:
        ct_list = cartlist.objects.filter(user=user)
        if ct_list.exists():
            for ct in ct_list:
                prod = get_object_or_404(product, id=product_id)
                try:
                    c_items = items.objects.get(prod=prod, cart=ct)
                    if c_items.quan > 1:
                        c_items.quan -= 1
                        prod.stock += 1
                        prod.save()
                        c_items.save()
                    else:
                        prod.stock += c_items.quan
                        prod.save()
                        c_items.delete()
                except items.DoesNotExist:
                    pass
    except cartlist.DoesNotExist:
        pass
    return redirect('cartDetails')

@login_required(login_url='login')
def delete_from_cart(request, product_id):
    user = request.user
    try:
        ct_list = cartlist.objects.filter(user=user)
        if ct_list.exists():
            for ct in ct_list:
                prod = get_object_or_404(product, id=product_id)
                try:
                    c_items = items.objects.get(prod=prod, cart=ct)
                    prod.stock += c_items.quan
                    prod.save()
                    c_items.delete()
                except items.DoesNotExist:
                    pass
    except cartlist.DoesNotExist:
        pass
    return redirect('cartDetails')

@login_required(login_url='login')
def cart_details(request, tot=0, count=0, cart_items=None):
    try:
        user = request.user
        if user.is_authenticated:
            ct = cartlist.objects.filter(user=user)
        else:
            cart_id = request.session.get('cart_id')
            ct = cartlist.objects.filter(cart_id=cart_id)

        ct_items = items.objects.filter(cart__in=ct, active=True)
        for i in ct_items:
            tot += (i.prod.price * i.quan)
            count += i.quan

    except ObjectDoesNotExist:
        return HttpResponse("<script> alert('Empty Cart');window.location='/';</script>")

    return render(request, 'cart.html', {'ci': ct_items, 't': tot, 'cn': count})

def checkout(request):
    if request.method == 'POST':
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        country = request.POST['country']
        address = request.POST['address']
        towncity = request.POST['city']
        postcodezip = request.POST['pin']
        phone = request.POST['phone']
        email = request.POST['email']
        cart = cartlist.objects.filter(user=request.user).first() # first() is used to get values added by user latestly

        check = Checkout(
            user=request.user,
            cart=cart,
            firstname=firstname,
            lastname=lastname,
            country=country,
            address=address,
            towncity=towncity,
            postcodezip=postcodezip,
            phone=phone,
            email=email
        )
        check.save()
        return redirect('payment')
    return render(request,'checkout.html')

def payment(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        name = request.POST.get('name')
        expiry_month = request.POST.get('expiry_month')
        expiry_year = request.POST.get('expiry_year')
        cvv = request.POST.get('cvv')

        pay = payment(
            user=request.user,
            account_number=account_number,
            name=name,
            expiry_month=expiry_month,
            expiry_year=expiry_year,
            cvv=cvv
        )
        pay.save()

        user = request.user
        ct = cartlist.objects.get(user=user)
        items.objects.filter(cart=ct).delete()

        return redirect ('successful')

    return render(request, 'bank.html')

def successful(request):
    return redirect('successful.html')