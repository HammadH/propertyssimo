from django.shortcuts import render_to_response
from django.views.generic import View

from listings.models import Listing

class Landing(View):
	def get(self, request, *args, **kwargs):
		featured_listings = Listing.objects.filter(is_featured=True, status=1)
		return render_to_response('landing.html', {'featured_listings':featured_listings})


