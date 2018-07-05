from airtable import Airtable
from .models import Category, Product
from django.shortcuts import render
import os



AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
              'Movies',
              api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query + "', {Name})")
    stuff_for_frontend = {"search_result": search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    context = {
        'product': product
    }
    return render(request, 'shop/product/detail.html', context)

