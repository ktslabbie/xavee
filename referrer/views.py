from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, RedirectView

from .models import Referral

class ReferralRedirectView(RedirectView):
    def get_redirect_url(self):
        referral = get_object_or_404(Referral, pk=self.request.GET.get('r'))
        referral.update_clicks()
        return referral.app.appstore_link

class HomepageView(TemplateView):
    template_name = "referrer_index.html"