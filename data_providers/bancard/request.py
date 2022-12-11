import hashlib

import requests

from core import settings


class BancardAPI:
    def __init__(self, bancard_url=settings.BANCARD_URL) -> None:
        self.bancard_url = bancard_url
        self.auth_headers = self.create_headers()
        self.public_key = settings.BANCARD_PUBLIC_KEY
        self.private_key = settings.BANCARD_PRIVATE_KEY
        self.currency = 'PYG'
        self.return_url = settings.DOMAIN_URI + settings.BANCARD_RETURN_URL
        self.cancel_url = settings.DOMAIN_URI + settings.BANCARD_CANCEL_URL

    def create_headers(self):
        return {
            'Content-Type': 'application/json'
        }

    def single_buy(self, shop_process_id, amount, description, phone_number=None):
        single_buy_url = self.bancard_url + '/vpos/api/0.3/single_buy'

        amount_str = f'{amount}.00'
        token = f'{self.private_key}{shop_process_id}{amount_str}{self.currency}'
        token = self.get_token(token)

        payload = {
            'public_key': self.public_key,
            'operation': {
                'token': token,
                'shop_process_id': shop_process_id,
                'currency': self.currency,
                'amount': amount_str,
                'additional_data': phone_number if phone_number else '',
                'description': description,
                'return_url': self.return_url,
                'cancel_url': self.cancel_url
            }
        }

        if phone_number:
            payload.get('operation').update({
                'zimple': 'S'
            })

        return requests.post(url=single_buy_url, headers=self.auth_headers, json=payload)

    def cards_new(self, card_id, user_id, phone_number, email_addr):
        cards_new_url = self.bancard_url + '/vpos/api/0.3/cards/new'

        token = f'{self.private_key}{card_id}{user_id}request_new_card'
        token = self.get_token(token)

        payload = {
            'public_key': self.public_key,
            'operation': {
                'token': token,
                'card_id': card_id,
                'user_id': user_id,
                'user_cell_phone': phone_number,
                'user_mail': email_addr,
                'return_url': self.return_url
            }
        }
        return requests.post(url=cards_new_url, headers=self.auth_headers, json=payload)

    def users_cards(self, user_id):
        users_cards_url = self.bancard_url + f'/vpos/api/0.3/users/{user_id}/cards'

        token = f'{self.private_key}{user_id}request_user_cards'
        token = self.get_token(token)

        payload = {
            'public_key': self.public_key,
            'operation': {
                'token': token
            }
        }
        return requests.post(url=users_cards_url, headers=self.auth_headers, json=payload)

    def charge(self, shop_process_id, amount, description, alias_token):
        charge_url = self.bancard_url + '/vpos/api/0.3/charge'

        amount_str = f'{amount}.00'
        token = f'{self.private_key}{shop_process_id}charge{amount_str}{self.currency}{alias_token}'
        token = self.get_token(token)

        payload = {
            'public_key': self.public_key,
            'operation': {
                'token': token,
                'shop_process_id': shop_process_id,
                'amount': amount_str,
                'number_of_payments': 1,
                'currency': self.currency,
                'additional_data': '',
                'description': description
            },
            'alias_token': alias_token
        }

        return requests.post(url=charge_url, headers=self.auth_headers, json=payload)

    def remove_card(self, user_id, alias_token):
        remove_card_url = self.bancard_url + f'/vpos/api/0.3/users/{user_id}/cards'

        token = f'{self.private_key}delete_card{user_id}{alias_token}'
        token = self.get_token(token)

        payload = {
            'public_key': self.public_key,
            'operation': {
                'token': token,
                'alias_token': alias_token
            }
        }

        return requests.delete(url=remove_card_url, headers=self.auth_headers, json=payload)

    def rollback(self, shop_process_id):
        rollback_url = self.bancard_url + '/vpos/api/0.3/single_buy/rollback'

        token = f'{self.private_key}{shop_process_id}rollback0.00'
        token = self.get_token(token)

        payload = {
            'public_key': self.public_key,
            'operation': {
                'token': token,
                'shop_process_id': shop_process_id
            }
        }

        return requests.post(url=rollback_url, headers=self.auth_headers, json=payload)

    def get_buy_single_confirmation(self, shop_process_id):
        confirmation_url = self.bancard_url + '/vpos/api/0.3/single_buy/confirmations'

        token = f'{self.private_key}{shop_process_id}get_confirmation'
        token = self.get_token(token)

        payload = {
            'public_key': self.public_key,
            'operation': {
                'token': token,
                'shop_process_id': shop_process_id
            }
        }

        return requests.post(url=confirmation_url, headers=self.auth_headers, json=payload)

    def get_token(self, token_str):
        return hashlib.md5(token_str.encode()).hexdigest()
