from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view




@api_view(['GET'])
def custom404(request, exception=None):
    data = {'message': 'The resource was not found'}
    return Response(data, status=status.HTTP_404_NOT_FOUND)

