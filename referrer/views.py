from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView, RedirectView
from core import dicts

from .models import Referral

# Create your views here.
def redirect(request):
    referral = get_object_or_404(Referral, pk=request.GET.get('r'))
    referral.update_clicks()
    return render(request, 'redirect.html', {'referral': referral})

# class ReferralRedirectView(TemplateView):
#     
#     def get_redirect_url(self):
#         referral = get_object_or_404(Referral, pk=self.request.GET.get('r'))        
#         referral.update_clicks()
#         
#         # Create your views here.
#         return render(request, 'redirect.html', {'referral': referral})
        
        #if referral.app.platform is dicts.ANDROID:
        #    return "https://play.google.com/store/apps/details?id=" + referral.app.bundle_id + "&hl=" + dicts.LANGUAGE_CODES.get(referral.app.country)
        #elif referral.app.platform is dicts.IPHONE:
        #    return "https://itunes.apple.com/" + referral.app.country + "/app/id" + str(referral.app.appstore_id) + "?mt=8"
        

class HomepageView(TemplateView):
    template_name = "referrer_index.html"