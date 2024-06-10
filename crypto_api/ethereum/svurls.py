# coins/vurls.py

from django.urls import path
from .views import CryptoDataView, CryptoDataResultView

urlpatterns = [
    path('crypto/', CryptoDataView.as_view(), name='crypto_data'),
    path('crypto/result/<task_id>/', CryptoDataResultView.as_view(), name='crypto_data_result'),
]
