from django.urls import path
from .views import create_transaction

urlpatterns = [
    path('transations', create_transaction, name='transactions')
]
