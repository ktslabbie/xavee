from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

class APIRootView(APIView):
    def get(self, request):
        return Response({
            #'posts':        reverse('post-list', request=request),
            'apps':         reverse('api:application-list', request=request),
            'developers':   reverse('api:developer-list', request=request),
            #'rankings':     reverse('application-ranking', request=request),
        })