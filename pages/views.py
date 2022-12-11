from django.shortcuts import render, get_object_or_404

from customers.forms import CustomerForm
from customers.models import Orders
from products.models import Product


# Create your views here.
def index(request):
    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'pages/index.html', context)


def checkout(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            new_customer = form.save()
    else:
        form = CustomerForm()

    context = {
        'form': form
    }

    return render(request, 'pages/checkout.html', context)


def order_pay(request, code):
    # order = get_object_or_404(Orders, code=code)

    context = {
        'process_id': 'iZQXZpaQJqkHzZH.9624'
    }

    return render(request, 'pages/order-pay.html', context)
