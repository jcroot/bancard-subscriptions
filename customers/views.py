from django.contrib import messages, auth
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from customers.models import CustomerCards, Profile, Orders
from data_providers.bancard.request import BancardAPI
from transactions.models import Transaction


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
                if card:
                    card.is_default = True
                    card.save(update_fields=['is_default'])  # select card by default
            elif option == 2:
                pass  # add new card
            elif option == 3:  # charge to the default card
                order = Orders.objects.get(pk=card_id)  # card_id change for generic id
                if order:
                    new_transaction = Transaction.objects.create_transaction(order=order)
                    if new_transaction:
                        response = BancardAPI().charge(shop_process_id=new_transaction.id,
                                                       amount=new_transaction.amount,
                                                       description=order.product_plan.plan.title_plan,
                                                       alias_token=new_transaction.card.alias_token,
                                                       number_of_payments=new_transaction.number_of_payments)

                        if response:
                            response_json = response.json()
                            if response_json['status'] == 'success':
                                if new_transaction.id == response_json['confirmation']['shop_process_id']:
                                    new_transaction.response = response_json['confirmation']['response']
                                    new_transaction.response_details = response_json['confirmation']['response_details']
                                    new_transaction.authorization_number = response_json['confirmation'][
                                        'authorization_number']
                                    new_transaction.ticket_number = response_json['confirmation']['ticket_number']
                                    new_transaction.response_code = response_json['confirmation']['response_code']
                                    new_transaction.response_description = response_json['confirmation'][
                                        'response_description']
                                    new_transaction.security_information = response_json['confirmation'][
                                        'security_information']
                                    new_transaction.save()

    cards = CustomerCards.objects.filter(customer__user=request.user).all()
    with transaction.atomic():
        for card in cards:
            card.update_alias_token()

        customer = Profile.objects.filter(user_id=request.user.id)
        if not customer:
            messages.error(request, "Usuario no existe o es admin")
            return redirect(reverse('index'))

    transactions = Transaction.objects.filter(order__profile=customer.first())
    transaction_data = None
    if transactions:
        transaction_data = transactions.all()

    context = {
        'cards': cards,
        'customer': customer,
        'orders': customer.get().orders_set.all(),
        'transactions': transaction_data
    }

    return render(request, 'pages/customer/profile.html', context)


def delete_card(request, card_id):
    if request.method == 'GET':
        card = CustomerCards.objects.get(pk=card_id)
        transactions = Transaction.objects.filter(card=card)
        if not transactions.exists():
            if card:
                response = BancardAPI().remove_card(user_id=card.customer_id, alias_token=card.alias_token)
                response_json = response.json()
                if response_json['status'] == 'success':
                    card.delete()
                    messages.success(request, "Tarjeta eliminada.", extra_tags="success")
                else:
                    messages.error(request, "La tarjeta no existe o hubo un error al eliminar.", extra_tags="danger")
        else:
            messages.error(request, "No se puede eliminar esta tarjeta por que tiene transacciones asociadas.")

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
