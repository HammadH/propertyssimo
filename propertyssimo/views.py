from django.shortcuts import render_to_response
from django.views.generic import View
from django.template import RequestContext
from django.db.models import Q

from listings.models import Listing

AREAS = set([listing.location for listing in Listing.objects.all()])

class Landing(View):
	def get(self, request, *args, **kwargs):
		featured_listings = Listing.objects.filter(is_featured=True, status=1)
		return render_to_response('landing.html', {'featured_listings':featured_listings})


class AboutUs(View):
	def get(self, request, *args, **kwargs):
		return render_to_response('about_us.html')


class Buyers(View):
	def get(self, request, *args, **kwargs):
		return render_to_response('buyers.html')


class Services(View):
	def get(self, request, *args, **kwargs):
		return render_to_response('services.html')		

class Careers(View):
	def get(self, request, *args, **kwargs):
		return render_to_response('careers.html')

class Selling(View):
	def get(self, request, *args, **kwargs):
		return render_to_response('selling.html')

class Investing(View):
	def get(self, request, *args, **kwargs):
		return render_to_response('investment.html')

class Vacation(View):
	def get(self, request, *args, **kwargs):
		return render_to_response('vacation.html')

class Renter(View):
	def get(self, request, *args, **kwargs):
		return render_to_response('letting.html')		


class Landlords(View):
	def get(self, request, *args, **kwargs):
		return render_to_response('landlords.html')

class SiteListings(View):
	def get(self, request, *args, **kwargs):
		listings = Listing.objects.all()
		AREAS = set([listing.location for listing in listings])
		
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

		min_price = request.GET.get('min_price', None)
		max_price = request.GET.get('max_price', None)

		if min_price or max_price:
			listings = listings.filter(Q(_price__gte=int(min_price)) & Q(_price__lte=int(max_price)))

		status = request.GET.get('status', None)
		if status:
			listings = listings.filter(status=status)

		area = request.GET.get('area', None)
		if area:
			listings = listings.filter(location=area)

		search_keyword = request.GET.get('search', None)
		if search_keyword:
			listings = listings.filter(Q(location__icontains=search_keyword) | Q(building__icontains=search_keyword)
				| Q(agent_email__icontains=search_keyword) | Q(refno__icontains=search_keyword))

		return render_to_response('marina.html', {'listings':listings, 'area_options':AREAS, 'area':'dubai'}, RequestContext(request))

class Marina(View):
	def get(self, request, *args, **kwargs):
		listings = Listing.objects.filter(location__icontains="Dubai Marina")

		
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

		min_price = request.GET.get('min_price', None)
		max_price = request.GET.get('max_price', None)

		if min_price or max_price:
			listings = listings.filter(Q(_price__gte=int(min_price)) & Q(_price__lte=int(max_price)))

		status = request.GET.get('status', None)
		if status:
			listings = listings.filter(status=status)

		area = request.GET.get('area', None)
		if area:
			listings = listings.filter(location=area)

		search_keyword = request.GET.get('search', None)
		if search_keyword:
			listings = listings.filter(Q(location__icontains=search_keyword) | Q(building__icontains=search_keyword)
				| Q(agent_email__icontains=search_keyword) | Q(refno__icontains=search_keyword))

		return render_to_response('marina.html', {'listings':listings, 'area_options':AREAS, 'area':'marina'}, RequestContext(request))

class JBR(View):
	def get(self, request, *args, **kwargs):
		listings = Listing.objects.filter(location__icontains="jumeirah beach residence")

		
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

		min_price = request.GET.get('min_price', None)
		max_price = request.GET.get('max_price', None)

		if min_price or max_price:
			listings = listings.filter(Q(_price__gte=int(min_price)) & Q(_price__lte=int(max_price)))

		status = request.GET.get('status', None)
		if status:
			listings = listings.filter(status=status)

		area = request.GET.get('area', None)
		if area:
			listings = listings.filter(location=area)

		search_keyword = request.GET.get('search', None)
		if search_keyword:
			listings = listings.filter(Q(location__icontains=search_keyword) | Q(building__icontains=search_keyword)
				| Q(agent_email__icontains=search_keyword) | Q(refno__icontains=search_keyword))

		return render_to_response('marina.html', {'listings':listings, 'area_options':AREAS, 'area':'jbr'}, RequestContext(request))

class Palm(View):
	def get(self, request, *args, **kwargs):
		listings = Listing.objects.filter(location__icontains="Palm jumeirah")

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

		min_price = request.GET.get('min_price', None)
		max_price = request.GET.get('max_price', None)

		if min_price or max_price:
			listings = listings.filter(Q(_price__gte=int(min_price)) & Q(_price__lte=int(max_price)))

		status = request.GET.get('status', None)
		if status:
			listings = listings.filter(status=status)

		area = request.GET.get('area', None)
		if area:
			listings = listings.filter(location=area)

		search_keyword = request.GET.get('search', None)
		if search_keyword:
			listings = listings.filter(Q(location__icontains=search_keyword) | Q(building__icontains=search_keyword)
				| Q(agent_email__icontains=search_keyword) | Q(refno__icontains=search_keyword))

		return render_to_response('marina.html', {'listings':listings, 'area_options':AREAS, 'area':'palm'}, RequestContext(request))

class Downtown(View):
	def get(self, request, *args, **kwargs):
		listings = Listing.objects.filter(location__icontains="Downtown Dubai")
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

		min_price = request.GET.get('min_price', None)
		max_price = request.GET.get('max_price', None)

		if min_price or max_price:
			listings = listings.filter(Q(_price__gte=int(min_price)) & Q(_price__lte=int(max_price)))

		status = request.GET.get('status', None)
		if status:
			listings = listings.filter(status=status)

		area = request.GET.get('area', None)
		if area:
			listings = listings.filter(location=area)

		search_keyword = request.GET.get('search', None)
		if search_keyword:
			listings = listings.filter(Q(location__icontains=search_keyword) | Q(building__icontains=search_keyword)
				| Q(agent_email__icontains=search_keyword) | Q(refno__icontains=search_keyword))

		return render_to_response('marina.html', {'listings':listings, 'area_options':AREAS, 'area':'downtown'}, RequestContext(request))