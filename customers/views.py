from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from customers.models import CustomerCards
from data_providers.bancard.request import BancardAPI


# Create your views here.
def profile(request):
    cards = CustomerCards.objects.filter(customer_id=3).all()

    context = {
        'cards': cards
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
    return render(request, 'pages/customer/login.html')