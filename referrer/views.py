from .models import Referral
from django.shortcuts import render, get_object_or_404

from django.views.generic import TemplateView

class HomepageView(TemplateView):
    template_name = "referrer_index.html"

# Create your views here.
def redirect(request, platform, app_name):
    referral = get_object_or_404(Referral, pk=request.GET.get('r'))
    return render(request, 'redirect.html', {'referral': referral})