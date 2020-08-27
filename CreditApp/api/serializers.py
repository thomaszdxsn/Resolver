from rest_framework import serializers


__all__ = ("CreateTransactionSerializer",)

class CreateTransactionSerializer(serializers.Serializer):
    card_seria_no = serializers.CharField(required=True, max_length=255)
    card_password = serializers.CharField(required=True, max_length=6)
    merchant_name = serializers.CharField(required=True, max_length=255)
    amount =serializers.DecimalField(max_digits=10, decimal_places=2)