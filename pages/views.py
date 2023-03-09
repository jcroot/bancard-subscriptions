from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from customers.forms import CustomerForm
from customers.models import Orders, CustomerCards, Cart, UserProfile, Profile
from data_providers.bancard.request import BancardAPI
from pages.forms import NewUserForm
from products.models import Product, PlanProducts


# Create your views here.
def index(request):
    products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'pages/index.html', context)


def checkout(request, code):
    cart = get_object_or_404(Cart, session_code=code)
    new_order = None
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if request.user.is_authenticated:
            product_plan = PlanProducts.objects.get(pk=cart.product_plan.id)
            user_profile = Profile.objects.filter(user_id=request.user.id).first()
            if user_profile:
                new_order = Orders.objects.create_order(profile=user_profile, product_plan=product_plan)
        else:
            if form.is_valid():
                user = UserProfile.objects.create_user(form.cleaned_data['email_address'], 'abcd1234')
                if user is not None:
                    form.cleaned_data['user_id'] = user.id
                    new_customer = form.save()

                    product_plan = PlanProducts.objects.get(pk=cart.product_plan.id)
                    new_order = Orders.objects.create_order(profile=new_customer, product_plan=product_plan)

        if new_order:
            return redirect(reverse('order-pay', kwargs={'code': new_order.order_code}))
    else:
        form = CustomerForm()

    context = {
        'form': form,
        'code': code,
        'product_plan': cart.product_plan,
    }

    return render(request, 'pages/checkout.html', context)


def order_pay(request, code):
    order = get_object_or_404(Orders, order_code=code)

    bancard = BancardAPI()

    customer_card = CustomerCards.objects.create(customer=order.profile)

    context = {
        'process_id': ''
    }

    response = bancard.cards_new(card_id=customer_card.id, user_id=order.profile.id,
                                 phone_number=order.profile.phone, email_addr=order.profile.email_address)

    if response:
        response_json = response.json()
        process_id = response_json['process_id']

        context.update({
            'process_id': process_id,
            'order': order
        })

    return render(request, 'pages/order-pay.html', context)


def card_return_url(request, card_id):
    context = {}
    if request.method == 'GET' and 'status' in request.GET:
        status = request.GET['status']

        if 'add_new_card_success' in status:
            customer_card = get_object_or_404(CustomerCards, pk=card_id)

            if customer_card:
                customer_card.update_alias_token(customer_card.customer.id)

                context.update({
                    'status': 'success',
                    'message': 'You card now is recorded'
                })

        if 'add_new_card_fail' in status:
            description = request.GET['description']

            context.update({
                'status': 'failed',
                'message': description
            })

    return render(request, 'pages/card-status.html', context)


def add_item_to_cart(request):
    if request.method == 'POST':
        plan_id = request.POST['plan_id']
        product_plan = PlanProducts.objects.get(pk=plan_id)

        cart = Cart.objects.create_cart(product_plan=product_plan)

        if cart:
            return redirect(reverse('checkout', kwargs={'code': cart.session_code}))


def confirm_payment(request):
    if request.method == 'POST':
        pass

    return {'hola': 'que tal'}
