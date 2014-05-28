from .models import Referral

# Create your views here.
from django.shortcuts import redirect

def redirect_to_store(request):
    
    # Retrieve the Referral object based on the GET parameters in the URL received.
    referral = Referral.objects.get(
        source = request.GET.get('utm_source', None),
        medium = request.GET.get('utm_medium', None),
        name   = request.GET.get('utm_campaign', None)
    )
    
    # Redirect to destination link.
    return redirect(referral.destination)