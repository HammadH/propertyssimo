import datetime
import re
from django.contrib import admin
from django.db import models
from django.core.urlresolvers import reverse



CITY_CODES = {
	2  :  'Dubai', 
	3  :  'Abu Dhabi', 
	11  :  'Ras al Khaimeh', 
	12  :  'Sharjah',
	13  :  'Fujeirah',
	14  :  'Ajman',
	15  :  'Umm al Quwain',
	39  :  'Al Ain'
}

class Listing(models.Model):
	agent_name = models.CharField(max_length=75, null=True, blank=True)
	agent_email = models.CharField(max_length=75, null=True, blank=True)
	agent_mobile = models.CharField(max_length=75, null=True, blank=True)
	status = models.CharField(max_length=75, null=True, blank=False)
	city = models.CharField(max_length=75, blank=False, null=True)
	type = models.CharField(max_length=75, blank=False, null=True)
	subtype = models.CharField(max_length=75, blank=False, null=True)
	commercialtype = models.CharField(max_length=75, blank=True, null=True)
	refno = models.CharField(unique=True, max_length=75, blank=False, null=True)
	title = models.CharField(max_length=225, blank=False, null=True)
	description = models.TextField(blank=True, null=True)
	size = models.CharField(max_length=75, blank=True, null=True)
	price = models.CharField(max_length=75, blank=False, null=True)
	bedrooms = models.CharField(max_length=75, blank=True, null=True)
	feed_lastupdated = models.CharField(max_length=75, blank=True, null=True)
	db_lastupdated = models.DateTimeField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	location = models.CharField(max_length=75, blank=True, null=True)
	building = models.CharField(max_length=75, blank=True, null=True)
	bathrooms = models.CharField(max_length=75, blank=True, null=True)
	amenities = models.CharField(max_length=75, blank=True, null=True)
	photos = models.TextField(blank=True, null=True)
	published_on_dbz = models.CharField(max_length=75, blank=True, null=True)
	published_on_pf = models.CharField(max_length=75, blank=True, null=True)
	published_on_bayut = models.CharField(max_length=75, blank=True, null=True)
	is_furnished = models.CharField(max_length=75, blank=True, null=True)
	is_featured = models.BooleanField(blank=True, default=False, null=False)
	

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.db_lastupdated = datetime.datetime.now()
		super(Listing, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		if self.published_on_dbz == 'False' and not self.published_on_pf:
			self.status = 0
			self.save()

		if self.published_on_pf == 'False' and not self.published_on_dbz:
			self.status = 0
			self.save()

		if self.published_on_dbz == 'False' and self.published_on_pf == 'False':
			self.status = 0
			self.save() 


	def hard_delete(self, *args, **kwargs):
		super(Listing, self).delete()

	def get_absolute_url(self):
		return reverse('listing_details', kwargs={'id':self.id})

	def create_or_update_from_dbz_xml(self, soup):
		self.status = 1
		self.agent_email = soup.contactemail.text
		if self.agent_email:
			self.agent_name = soup.contactemail.text.split('@')[0]
		self.agent_mobile = soup.contactnumber.text
		self.city = CITY_CODES[int(soup.city.text)]
		self.type = soup.type.text
		self.subtype = soup.subtype.text
		if soup.commercialtype:
			self.commercialtype = soup.commercialtype.text
		self.refno = soup.refno.text
		self.title = soup.title.text
		self.description = soup.description.text
		self.size = soup.size.text if soup.size else None
		self.price = soup.price.text
		if soup.bedrooms:
			self.bedrooms = soup.bedrooms.text
		#parse lastupdate and convert to datetime
		self.feed_lastupdated = soup.lastupdated.text
		self.location = soup.locationtext.text if soup.locationtext else None
		self.building = soup.building.text if soup.building else None
		if soup.bathrooms:
			self.bathrooms = soup.bathrooms.text
		if soup.amenities:
			self.amenities = parse_dbz_amenities(soup.amenities.text)
		if soup.photos:
			self.photos = soup.photos.text
		return self


	def create_or_update_from_pf_xml(self, soup):
		self.status = 1
		self.agent_email = soup.agent.email.text.strip()
		self.agent_name = soup.agent.find('name').text.strip()
		self.agent_mobile = soup.agent.phone.text.strip()
		self.city = soup.city.text
		#converting type and subtype to dbz format
		category = soup.offering_type.text.strip()
		type = soup.property_type.text.strip()
		if category == 'RR':
			self.type = 'RP'
			if type == 'AP':
				self.subtype = 'AP'
			elif type == 'VH':
				self.subtype = 'VI'
		elif category == 'RS':
			self.type = 'SP'
			if type == 'AP':
				self.subtype = 'AP'
			elif type == 'VH':
				self.subtype = 'VI'
		elif category == 'CR':
			self.type = 'RP'
			self.subtype = 'CO'
			if type == 'OF':
				self.commercialtype = 'OF'
			elif type == 'RE':
				self.commercialtype = 'RE'
			elif type == 'ST':
				self.commercialtype = 'ST'
			elif type == 'WH':
				self.commercialtype = 'IN'
		elif category == 'CS':
			self.type = 'SP'
			self.subtype = 'CO'
			if type == 'OF':
				self.commercialtype = 'OF'
			elif type == 'RE':
				self.commercialtype = 'RE'
			elif type == 'ST':
				self.commercialtype = 'ST'
			elif type == 'WH':
				self.commercialtype = 'IN'
		self.refno = soup.reference_number.text.strip()
		self.title = soup.title_en.text.strip()
		self.description = soup.description_en.text.strip()
		self.size = soup.size.text.strip() if soup.size else None
		self.price = soup.price.text.strip()
		if soup.bedroom:
			if soup.bedroom.text.strip() == 'studio':
				self.bedrooms = 0
			else:
				self.bedrooms = soup.bedroom.text.strip()
		#parse lastupdate and convert to datetime
		# self.feed_lastupdated = soup.lastupdated.text
		self.location = soup.community.text.strip() if soup.community else None
		self.building = soup.property_name.text.strip() if soup.property_name else None
		if soup.bathroom:
			self.bathrooms = soup.bathroom.text.strip()
		# if soup.amenities:
		# 	self.amenities = parse_dbz_amenities(soup.amenities.text)

		photos = soup.photo
		if photos:
			_photos = []
			for i in photos.contents:
				if i != '\n':
					_photos.append(i.string.strip())
			self.photos = ''
			for key,photo in enumerate(_photos):
				self.photos += photo
				if (key+1) < len(_photos):
					self.photos += '|'
		return self


	def get_absolute_url(self, *args, **kwargs):
		return reverse('listing_details', kwargs={'id':self.id})

	def get_thumbnail_image(self):
		if self.photos:
			return self.photos.split('|')[0]
		else: return None

	def get_agent_shortname(self):
		return self.agent_name.strip().split(' ')[0]







admin.site.register(Listing)