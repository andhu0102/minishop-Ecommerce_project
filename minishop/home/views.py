from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import *
# Create your views here.
def home (request,c_slug=None):

    if c_slug!=None:
        c_page = get_object_or_404(cate, slug=c_slug)
        prodt = product.objects.filter(category=c_page, available=True)
    else:
        prodt = product.objects.all().filter(available=True)

    paginator = Paginator(prodt, 1)  # number of products in a page
    page = request.GET.get('page')
    paginated = paginator.get_page(page)

    cata = cate.objects.all()
    return render(request, 'index.html', {'c': cata, 'p': prodt, "paginated":paginated})

def details(request,c_slug,product_slug):
    prodt = get_object_or_404(product, category__slug=c_slug, slug=product_slug)
    return render(request, 'product-single.html', {'pro': prodt})

def searching(request):
    if 'q' in request.GET:
        query = request.GET.get('q')      #to store data in search box

        prod = product.objects.all().filter(Q(name__icontains=query)|Q(desc__icontains=query),available=True)
    return render(request, 'search.html',{'pr':prod})
