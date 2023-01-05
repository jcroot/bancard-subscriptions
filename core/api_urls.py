from rest_framework import routers
from django.urls import include, path

from transactions.views import TransactionViewSet

PREFIX = "api"

router = routers.DefaultRouter()
router.register(r'confirm', TransactionViewSet, 'transactions')

urlpatterns = [
    path(f"{PREFIX}/", include(router.urls)),
]
