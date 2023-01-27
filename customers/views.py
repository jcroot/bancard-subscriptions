from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from customers.models import CustomerCards, Profile
from data_providers.bancard.request import BancardAPI


# Create your views here.
@login_required(login_url='/customer/login')
def profile(request):
    if request.method == "POST":
        option = request.POST["selector"]
        card_id = request.POST["card_select_id"]

        option = int(option)
        if int(option) > 0:
            if option == 1:
                card = CustomerCards.objects.get(pk=card_id)
                card.is_default = True
                card.save(update_fields=['is_default']) # select card by default
            elif option == 2:
                pass # add new card

    cards = CustomerCards.objects.filter(customer__user=request.user).all()
    customer = Profile.objects.get(user_id=request.user.id)

    context = {
        'cards': cards,
        'customer': customer,
        'orders': customer.orders_set.all()
    }

    return render(request, 'pages/customer/profile.html', context)


def delete_card(request, card_id):
    if request.method == 'GET':
        card = CustomerCards.objects.get(pk=card_id)
        if card:
            response = BancardAPI().remove_card(user_id=card.customer_id, alias_token=card.alias_token)
            response_json = response.json()
            if response_json['status'] == 'success':
                card.delete()
                messages.success(request, "Tarjeta eliminada.", extra_tags="success")
            else:
                messages.error(request, "La tarjeta no existe o hubo un error al eliminar.", extra_tags="danger")

            return redirect(reverse('profile'))


def login(request):
    if request.method == 'POST':
        username = request.POST['emailAddress']
        password = request.POST['password']
        code = request.POST['code']

        user = auth.authenticate(email=username.lower(), password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Your are now logged in')
            if code:
                return redirect(reverse('checkout', kwargs={'code': code}))
            else:
                return redirect(reverse('profile'))
        else:
            messages.error(request, 'Invalid credentials')
            if code:
                return redirect(reverse('checkout', kwargs={'code': code}))

    return render(request, 'pages/customer/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'Your are now logged out')
    return redirect('index')
