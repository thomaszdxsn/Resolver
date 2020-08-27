from decimal import Decimal

from django import db
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.decorators import api_view, throttle_classes, parser_classes
from rest_framework.parsers import JSONParser

from .serializers import CreateTransactionSerializer
from .models import Transaction, Card, Merchant


__all__ = ("merchant_auth", "create_transaction")


class TransactionThrottle(AnonRateThrottle):
    scope = 'transactions:create'
    rate = '10/sec'


@api_view(['POST'])
@parser_classes([JSONParser])
@throttle_classes([TransactionThrottle])
def create_transaction(request):
    payload_serializer = CreateTransactionSerializer(data=request.data)
    payload_serializer.is_valid(raise_exception=True)
    payload = payload_serializer.data

    card = Card.objects.filter(seria_no=payload['card_seria_no']).first()
    amount = Decimal(payload['amount'])
    if not card:
        return Response({"message": 'card not found'}, status=404)
    if card.password != payload['card_password']:
        return Response({"authorized": False}, status=401)
    merchant = Merchant.objects.filter(name=payload['merchant_name']).first()
    if not merchant:
        return Response({"message": 'merchant not found'}, status=404)
    
    with db.transaction.atomic():
        card = Card.objects.select_for_update().get(id=card.id)
        if card.amount < amount: 
            return Response({"message": "out of balance"}, status=400)
        transaction = Transaction.objects.create(
            merchant=merchant,
            card=card,
            amount=amount
        )
        card.amount -= transaction.amount
        card.save()
    return Response(data={
        'ok': True,
        'amount': transaction.amount,
        'created_at': transaction.created_at
    })