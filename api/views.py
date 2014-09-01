from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

class APIRootView(APIView):
    def get(self, request):
        return Response({
            'users': reverse('user-list', request=request),
            'posts': reverse('post-list', request=request),
            'apps': reverse('application-list', request=request),
        })
    