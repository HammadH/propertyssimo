from django.shortcuts import render_to_response
from django.views.generic import View
from django.template import RequestContext
from django.db.models import Q

from listings.models import Listing

import os
import csv
from datetime import datetime, date
from cStringIO import StringIO
from PIL import Image, ImageEnhance

from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.core.mail import send_mail


from bs4 import BeautifulSoup, CData

bufsize = 0 # making file unbuffered


DALY = 'daly@propertyissmo.com'
PROPPIX = 'support@prop-pix.com'

CITY_CODES = {
  'dubai':2,
  'abu dhabi':3,
  'aas al khaimeh':11,
  'sharjah':12,
  'fujeirah':13,
  'ajman':14,
  'umm al quwain':15,
  'al ain':39
				}


TYPE_SALE = ['s', 'S']
TYPE_RENT = ['r','R']
COMMERCIAL_CODES = ['RE', 'OF', 'IN', 'ST', 're', 'of', 'in', 'st']
SUBTYPE_COMMERCIAL = ['CO', 'co']
MULTIPLE_UNITS = ['BU', 'bu']
LAND_FOR_SALE = ['LA', 'la']
APARTMENT = ['ap', 'AP']
VILLA = ['vi', 'VI']

DBZ_AMENITIES = {'balcony': 'BA',
 'built in kitchen appliances': 'BK',
 'built in wardrobes': 'BW',
 'central a/c & heating': 'AC',
 'concierge service': 'CS',
 'covered parking': 'CP',
 'maid service': 'MS',
 'maids room': 'MR',
 'pets allowed': 'PA',
 'private garden': 'PG',
 'private gym': 'PY',
 'private jacuzzi': 'PJ',
 'private pool': 'PP',
 'security': 'SE',
 'shared gym': 'SY',
 'shared pool': 'SP',
 'shared spa': 'SS',
 'study': 'ST',
 'view of landmark': 'BL',
 'view of water': 'VW',
 'walk': 'WC',
 'dining in building': 'DB',
 'retail in building': 'RB',
 'available network': 'AN',
 'available furnished': 'AF',
 'conference room': 'CR',
 'furnished': 1 }

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

		status = request.GET.get('status', None)
		if status:
			listings = listings.filter(status=status)

		published = request.GET.get('published', None)
		if published:
			listings = listings.filter(Q(published_on_dbz=published) | Q(published_on_pf=published) | Q(published_on_bayut=published))

		search_keyword = request.GET.get('search', None)
		if search_keyword:
			listings = listings.filter(Q(location__icontains=search_keyword) | Q(building__icontains=search_keyword)
				| Q(agent_email__icontains=search_keyword) | Q(refno__icontains=search_keyword))

		return render_to_response('listings.html', {'listings':listings}, RequestContext(request))
		

show_listings = ShowListings.as_view()

class ListingDetails(View):
	def get(self, request, *args, **kwargs):
		listing = Listing.objects.get(id=kwargs.get('id'))
		if listing.photos:
			photos = [photo for photo in listing.photos.split('|')]
			return render_to_response('listing_details.html', {'listing':listing, 'photos':enumerate(photos), 'photos_copy':enumerate(photos)},RequestContext(request))
		else:
			 return render_to_response('listing_details.html', {'listing':listing}, RequestContext(request))

listing_details = ListingDetails.as_view()


class Platform(View):

	def post(self, request, *args, **kwargs):
		print 'got post'
		soup = BeautifulSoup(request.POST.get('<?xml version', None))
		try:
			agent_email = soup.find('email').text
		except:
			agent_email = None
		if soup is None:
			print "soup returned none"
			return Http404('Soup returned None')
		else:
			listing, errors = convert_to_platform(soup)
			if errors:
				send_mail('%s: Listing has errors' %ref_no, 'Please take care of the following \n %s' %[error for error in errors],
					 PROPPIX, [agent_email,])
				
			if listing:
				try:
					listing.save()
				except Exception, e:
					print e
				return HttpResponse(status=201)
						#return HttpResponse(dbz_soup, content_type="application/xhtml+xml")
			else:
				return Http404('Listing is None')

create_listing = Platform.as_view()

def convert_to_platform(soup):
		errors = []
		#soup is Beautifulsoup
		MLSNumber = soup.find('mlsnumber')

		if MLSNumber is not None:
				# varaible to use in emails. 
				#start by creating a parent <property> tag
				_mls = MLSNumber.text.strip()

				try:
					listing = Listing.objects.get(refno=_mls)
				except Listing.DoesNotExist:
					listing = Listing()

					#calculate the ref_no
					codes = _mls.split('-')
					if codes[0] in TYPE_RENT:
						listing.type = "RP"
					elif codes[0] in TYPE_SALE:
							listing.type = "SP"
					else:
							#log and email
							err = "%s Wrong MLS number or special characters in Description." %_mls
							errors.append(err)
							print err
							return (None, errors)
					
					if codes[1] in APARTMENT:
							listing.subtype = "AP"
					elif codes[1] in VILLA:
							listing.subtype = "VI"
					elif codes[1] in SUBTYPE_COMMERCIAL:
							if codes[2] not in COMMERCIAL_CODES or not codes[2]:
									err = "%s Incorrect or no commercial code" %_mls
									errors.append(err)
									print err
									return (None, errors)
							else:
									listing.subtype = "CO"
									listing.commercialtype = codes[2].upper()

					elif codes[1] in MULTIPLE_UNITS and codes[0] in TYPE_SALE:
							listing.subtype = "BU"
					elif codes[1] in LAND_FOR_SALE and codes[0] in TYPE_SALE:
							listing.subtype = "LA"
					else:
							err = 'Incorrect or missing subtype code. Wrong MLSNumber! Please check codes'
							errors.append(err)
							return (None, errors)

					listing.refno = _mls

		else:
			err = 'MLSNumber is empty or special characters in description.'
			errors.append(err)
			return (None, errors)

		## status tag ##
		status = soup.find('listingstatus')
		if status:
			if status.text == 'Active':
				listing.status = 1
			else:
				listing.status = 0
		else:
			err = "Listing status is empty. Please specify if it is active or closed."
			errors.append(err)
			return (None, errors)

		## title tag
		
		title = soup.find('streetname')
		if title:
			listing.title = title.text
		else:
			err = "Title is empty. Please fill it up in Street Name."
			errors.append(err)
			return (None, errors)


		## CDATA description tag
		description = soup.find('publicremark')
		if description:
				listing.description = description.text
		else: 
			err = "Listing has no description. Please fill up public remarks."
			errors.append(err)
			return (None, errors) # description is required field

		## city tag ##
		city = soup.find('city')
		if city:
			if city.text.lower() in CITY_CODES.keys():
				city_code = CITY_CODES[city.text.lower()]
				listing.city = str(city_code)
			else:
				err = "Incorrect city name"
				errors.append(err)
				return (None, errors)
		else:
			err =  "City name is empty. Please provide one." 
			errors.append(err)
			return (None, errors)

		## size ##
		size = soup.find('squarefeet')
		if size:
			listing.size = size.text
		else: 
			err =  "Square feet is empty, please fill it up."
			errors.append(err)
			return (None, errors)

		## price ##
		price = soup.find('listprice')
		if price:
			listing.price = price.text
		else:
			err = "List price is empty"
			errors.append(err)
			return (None, errors)

		## location ##
		location_text = soup.find('listingarea')
		if location_text:
			listing.location = location_text.text
		else:
			err = "Area name is empty."
			errors.append(err)
			return (None, errors)

		## building ##
		building = soup.find('buildingfloor')
		if building:
			listing.building = building.text
		else:
			err = "Building name is empty. Please fill buildingfloor"
			errors.append(err)
	
		## lastupdate ##
		listing.feed_lastupdated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
		
		## contactemail ##
		email = soup.find('email')
		if email:
			listing.agent_email = email.text
			listing.agent_name = email.text.split('@')[0]
		else:
			err = 'email is empty'
			errors.append(err)

		## contactnumber ##
		cellphone = soup.find('cellphone')
		if cellphone:
				listing.agent_mobile = cellphone.text
		else:
			err = 'mobile number is empty'
			errors.append(err)
		## images ##

		images = soup.find_all('picture')
		if images:
				print 'calling build_images'
				image_urls = build_images(images, refno=MLSNumber.text)
				if image_urls:
						
						if len(image_urls) == 1:
								listing.photos = image_urls[0]
						if len(image_urls) > 1:
								url_string = ""
								for url in image_urls[:len(image_urls)-1]:
										url_string += url + '|'
								url_string += image_urls[-1]
								listing.photos = url_string

		## bedrooms ##                        
		if listing.subtype in VILLA or listing.subtype in APARTMENT:
			bedrooms = soup.find('bedrooms')
			if bedrooms:
				if bedrooms.text != '100':
					listing.bedrooms = bedrooms.text
				elif bedrooms.text == '100':
					listing.bedrooms = '0'
			else:
				err = "No.of bedrooms is not provided. Please specify a number or 100 for studio"
				errors.append(err)
				return (None, errors)

		## bathrooms ##
		bathrooms = soup.find('bathtotal')
		if bathrooms:
			listing.bathrooms = bathrooms.text
		else:
			err = "No.of bathrooms is empty"
			errors.append(err)

		## ameneties ##
		amenities = []
		parking = soup.find('parking')
		try:
			parking_contents = parking.contents
			for content in parking_contents:
				if content.text == 'Yes':
					amenities.append('CP')
					break
		except:
			pass

		ac = soup.find('cooling')
		if ac:
			amenities.append('AC')

		features = soup.find_all('feature')
		if features:
			for feature in features:
				print '%s checking features' %_mls
				if feature.text in DBZ_AMENITIES.keys():
					if feature.text.lower() == 'furnished':
						listing.is_furnished = '1'
					else:
						amenities.append(DBZ_AMENITIES[feature.text.lower()])
	
		print 'checking private'
		if len(amenities) == 1:
			amenities = amenities[0]
		elif len(amenities) > 1:
			amenities_string = ''
			for a in amenities[:len(amenities)-1]:
				amenities_string += a + '|'
				amenities_string += amenities[-1]
				amenities = amenities_string
		else:
			amenities = ''

		listing.amenities = amenities

		print 'returning listing'
		return (listing, errors)


def build_image_path(refno, imgId=None, imgCaption=None):
		print 'going in build image path'
		if imgId is not None:
				folder_path = "/%s/%s/" %(date.today(), refno)
				folder_path = folder_path.replace(' ', '_')
				print folder_path
				try:
						os.makedirs(settings.MEDIA_ROOT+folder_path)
				except Exception, e:
						print e
				paths = {
				'full_img_path' : settings.MEDIA_ROOT + folder_path + imgId,
				'media_path' : "media" + folder_path + imgId
				}

				return paths

def watermark_image(image):
	image = image.convert('RGB')
	watermark = Image.open(settings.WATERMARK).convert("RGBA")
	alpha = watermark.split()[3]
	alpha = ImageEnhance.Brightness(alpha).enhance(settings.WATERMARK_OPACITY)
	watermark.putalpha(alpha)
	layer = Image.new("RGBA", image.size, (0,0,0,0))
	#positioning in center
	watermark_position = (image.size[0]/2-watermark.size[0]/2, image.size[1]/2-watermark.size[1]/2)
	layer.paste(watermark, watermark_position)
	return Image.composite(layer, image, layer)

def build_images(images, refno):
		"""
		<picture>
		<pictureid>
		<picturecaption>
		<contentytype>
		<binarydata>
		"""
		image_urls = []
		for image in images:
				try:
					content_type = image.contenttype.text
					encoded_data = image.binarydata.string.replace(' ','+')
					decoded_data = encoded_data.decode('base64')
					print 'decoded'
					imgfile = StringIO(decoded_data)
					img = Image.open(imgfile)
					print 'image opened'
					imgId = image.pictureid.text.strip('{,}')
					imgCaption = image.picturecaption.text
					img_paths = build_image_path(refno, imgId, imgCaption)
					full_img_path = img_paths['full_img_path'] + '.' + content_type.lower()

					try:
						image_exists = open(full_img_path, 'r')
					except IOError:
						print 'watermarking image'
						img = watermark_image(img)
						print 'watermarking complete'
						print 'saving image %s' %full_img_path
						img.save(full_img_path)
						print 'save comple.'
					image_xml_url = settings.DOMAIN_NAME + img_paths['media_path'] + '.' + content_type.lower()
					image_urls.append(image_xml_url)
				except Exception,e:
						print e
						continue
		return image_urls
