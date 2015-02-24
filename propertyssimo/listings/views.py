from django.shortcuts import render_to_response
from django.views.generic import View
from django.template import RequestContext
from django.db.models import Q

from listings.models import Listing

# type_dict = {
# 	'RP':['RP', 'for Rent'],
# 	'SP':['SP', 'for Sale'],
# }

# subtype_dict = {
# 	'AP':['AP', 'Apartment'],
# 	'VI':['VI', 'Villa'],
# 	'CO':['CO', 'Commercial']
# }

# commercial_dict = {
# 	'OF':['OF', 'Office'],
# 	'RE':['RE', 'Retail'],
# 	'ST':['ST', 'Staff'],
# 	'IN':['IN', 'Warehouse']
# }

class ShowListings(View):
	def get(self, request, *args, **kwargs):
		listings = Listing.objects.all()
		
		type = request.GET.get('type', None)
		if type:	
			listings = listings.filter(type=type)

		subtype = request.GET.get('subtype', None)
		if subtype:

			if 'CO' in subtype:
				subtype_code, commmercial_code = subtype.split('-')
				listings = listings.filter(Q(subtype=subtype_code)  & Q(commercialtype=commmercial_code))
			else:
				listings = listings.filter(subtype=subtype)

		bedrooms = request.GET.get('br', None)
		if bedrooms:
			listings = listings.filter(bedrooms=bedrooms)

		search_keyword = request.GET.get('search', None)
		if search_keyword:
			listings = listings.filter(Q(location__icontains=search_keyword) | Q(building__icontains=search_keyword)
				| Q(agent_email__icontains=search_keyword) | Q(refno__icontains=search_keyword))

		return render_to_response('listings.html', {'listings':listings}, RequestContext(request))

show_listings = ShowListings.as_view()

class ListingDetails(View):
	def get(self, request, *args, **kwargs):
		listing = Listing.objects.get(id=kwargs.get('id'))
		photos = [photo for photo in listing.photos.split('|')]
		return render_to_response('listing_details.html', {'listing':listing, 'photos':enumerate(photos), 'photos_copy':enumerate(photos)},RequestContext(request))

listing_details = ListingDetails.as_view()