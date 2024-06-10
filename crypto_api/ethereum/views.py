# dcoins/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import get_crypto_data
from celery.result import AsyncResult

class CryptoDataView(APIView):
    def post(self, request, *args, **kwargs):
        coin_symbols = request.data.get('coins', [])
        if not coin_symbols:
            return Response({'error': 'No coin symbols provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        task = get_crypto_data.delay(coin_symbols)
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)

class CryptoDataResultView(APIView):
    def get(self, request, task_id, *args, **kwargs):
        result = AsyncResult(task_id)
        if result.state == 'PENDING':
            return Response({'state': result.state}, status=status.HTTP_200_OK)
        elif result.state != 'FAILURE':
            return Response({'state': result.state, 'result': result.result}, status=status.HTTP_200_OK)
        else:
            return Response({'state': result.state, 'result': str(result.info)}, status=status.HTTP_200_OK)


