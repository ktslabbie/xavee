from .models import Referral

# Create your views here.
from django.shortcuts import redirect

def redirect_to_store(request, origin, app_title):
    
    redirect_object = Referral.objects.get(app_title=app_title)
    redirect_object.click_number += 1
    redirect_object.save()
    
    return redirect(redirect_object.destination)