from django.contrib import messages, auth
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customers.models import CustomerCards, Profile, Orders
from customers.serializers import CustomerSerializer, CardSerializer
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

                        response_json = response.json()
                        if response.status_code == 200:
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

                        else:
                            new_transaction.response_description = response_json['messages'][0]['dsc']
                            messages.error(request,
                                           "Ocurrio un error. La tarjeta no existe o faltaria actualizar el token")

                        new_transaction.save()

    cards = CustomerCards.objects.filter(customer__user=request.user)
    if cards:
        with transaction.atomic():
            for card in cards.all():
                card.update_alias_token()

    customer = Profile.objects.filter(user_id=request.user.id).first()
    if customer:
        transactions = Transaction.objects.filter(order__profile=customer)
        transaction_data = None
        if transactions:
            transaction_data = transactions.all()

    else:
        messages.error(request, "Usuario no existe o es admin")
        return redirect(reverse('index'))

    context = {
        'cards': cards,
        'customer': customer,
        'orders': customer.orders_set.all() if customer else [],
        'transactions': transaction_data
    }

    return render(request, 'pages/customer/profile.html', context)


def delete_card(request, card_id):
    if request.method == 'GET':
        try:
            card = CustomerCards.objects.get(pk=card_id)
            # eliminate from Bancard first, and remove default to use this card
            if card.alias_token:
                response = BancardAPI().remove_card(user_id=card.customer_id, alias_token=card.alias_token)
                response_json = response.json()
                if response_json['status'] == 'success':
                    card.alias_token = None
                    card.is_default = False
                    card.card_is_deleted = True
                    card.save()
                    messages.success(request, "Tarjeta eliminada.", extra_tags="success")
                else:
                    messages.error(request, response_json['status'])
        except CustomerCards.DoesNotExist:
            card = None

        return redirect(reverse('profile'))


def default_card(request):
    if request.method == 'POST':
        # first check is card exists
        card_id = request.POST.get('card_id')
        card_data = get_object_or_404(CustomerCards, pk=card_id)
        if card_data:
            # second update all cards with is_default = False
            update_cards_default_false(request.user)
            card_data.is_default = True
            # update this card with default = True
            card_data.save(update_fields=['is_default'])

            return JsonResponse({'status': 'success', 'card_id': card_id})

        return JsonResponse({'status': 'error'})

    return redirect(reverse('profile'))


def update_cards_default_false(user):
    cards = CustomerCards.objects.filter(customer__user=user)
    if cards:
        cards.update(is_default=False)


def rollback(request, transaction_id):
    transaction_data = Transaction.objects.get(pk=transaction_id)
    if transaction_data:
        response = BancardAPI().rollback(transaction_id)
        response_json = response.json()
        if response_json['status'] == 'success':
            messages.success(request, "Rollback exitoso.", extra_tags="success")
        else:
            messages.error(request, response_json['messages'][0]['dsc'])

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


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Profile.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        request.data.update({'user_id': token.user_id})

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        request.data.update({'user_id': token.user_id})

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardNewViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = CustomerCards.objects.all()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        alias_token = serializer.update_alias_token(kwargs['pk'])
        return Response({'alias_token': alias_token}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if 'customer_id' in request.data:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                process_id = serializer.create_new_card()
                return Response({
                    'process_id': process_id,
                    'url_redirect': f'/checkout/register_card/new?process_id={process_id}'
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
