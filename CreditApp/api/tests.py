import pytest
from django.core.cache import cache
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from .models import Card, Merchant, Transaction

TRANSACTION_ENDPOINT = reverse('transactions')

@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def mock_card(db):
    seria_no = '1234567'
    password = '123456'
    amount = 1000
    return Card.objects.create(seria_no=seria_no, password=password, amount=1000)


@pytest.fixture
def mock_merchant(db):
    return Merchant.objects.create(name='test-merchant')


def test_create_transaction_fail_if_invalid_request_payload(api_client):
    response = api_client.post(
        TRANSACTION_ENDPOINT,
        data={
            'card_seria_no': 123,
        },
        format='json'
    )
    assert response.status_code == 400


def test_create_transaction_fail_if_not_exists_card(api_client, mock_merchant):
    response = api_client.post(
        TRANSACTION_ENDPOINT,
        data={
            'card_seria_no': 'xxxx',
            'card_password': 'xxxx',
            'merchant_name': mock_merchant.name,
            'amount': 10
        },
        format='json'
    )
    assert response.status_code == 404


def test_create_transaction_fail_if_not_exists_merchant(api_client, mock_card):
    response = api_client.post(
        TRANSACTION_ENDPOINT,
        data={
            'card_seria_no': mock_card.seria_no,
            'card_password': mock_card.password,
            'merchant_name': 'xxx',
            'amount': 10
        },
        format='json'
    )
    assert response.status_code == 404

def test_create_transaction_fail_if_password_not_match(api_client, mock_card, mock_merchant):
    response = api_client.post(
        TRANSACTION_ENDPOINT,
        data={
            'card_seria_no': mock_card.seria_no,
            'card_password': 'xxxxxx',
            'merchant_name': mock_merchant.name,
            'amount': 10
        },
        format='json'
    )
    assert response.status_code == 401


def test_create_transaction_fail_if_no_enough_balance(api_client, mock_merchant, mock_card):
    response = api_client.post(
        TRANSACTION_ENDPOINT,
        data={
            'card_seria_no': mock_card.seria_no,
            'card_password': 'xxxxxx',
            'merchant_name': mock_merchant.name,
            'amount': 1001
        },
        format='json'
    )
    assert response.status_code == 401


def test_create_transaction_successful(api_client, mock_card, mock_merchant):
    response = api_client.post(
        TRANSACTION_ENDPOINT,
        data={
            'card_seria_no': mock_card.seria_no,
            'card_password': mock_card.password,
            'merchant_name': mock_merchant.name,
            'amount': 10
        },
        format='json'
    )

    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data['ok'] is True
    assert Transaction.objects.count() == 1



def test_create_transaction_throttle_after_10_times_1_sec(api_client, mock_card, mock_merchant):
    for _ in range(11):
        response = api_client.post(
        TRANSACTION_ENDPOINT,
        data={
            'card_seria_no': mock_card.seria_no,
            'card_password': mock_card.password,
            'merchant_name': mock_merchant.name,
            'amount': 10
        },
        format='json'
       )

    assert response.status_code == 429