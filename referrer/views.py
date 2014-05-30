from .models import Referral
from django.shortcuts import render, get_object_or_404

# Create your views here.
def redirect(request, platform, app_name):
    referral = get_object_or_404(Referral, pk=request.GET.get('r'))
    return render(request, 'redirect.html', {'referral': referral})