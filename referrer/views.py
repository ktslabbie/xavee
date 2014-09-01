from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, RedirectView
from core import dicts

from .models import Referral

class ReferralRedirectView(RedirectView):
    def get_redirect_url(self):
        referral = get_object_or_404(Referral, pk=self.request.GET.get('r'))
        referral.update_clicks()
        
        if referral.app.platform is dicts.ANDROID:
            return "https://play.google.com/store/apps/details?id=" + referral.app.bundle_id + "&hl=" + dicts.LANGUAGE_CODES.get(referral.app.country)
        elif referral.app.platform is dicts.IPHONE:
            return "https://itunes.apple.com/" + dicts.LANGUAGE_CODES.get(referral.app.country) + "/app/minecraft-pocket-edition/id" + str(referral.app.appstore_id) + "?mt=8"
        

class HomepageView(TemplateView):
    template_name = "referrer_index.html"