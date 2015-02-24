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
	commercialtype = models.CharField(max_length=75, blank=False, null=True)
	refno = models.CharField(unique=True, max_length=75, blank=False, null=True)
	title = models.CharField(max_length=225, blank=False, null=True)
	description = models.TextField(blank=True, null=True)
	size = models.CharField(max_length=75, blank=False, null=True)
	price = models.CharField(max_length=75, blank=False, null=True)
	bedrooms = models.CharField(max_length=75, blank=False, null=True)
	feed_lastupdated = models.CharField(max_length=75, null=True)
	db_lastupdated = models.DateTimeField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	location = models.CharField(max_length=75, blank=False, null=True)
	building = models.CharField(max_length=75, blank=False, null=True)
	bathrooms = models.CharField(max_length=75, blank=False, null=True)
	amenities = models.CharField(max_length=75, blank=False, null=True)
	photos = models.TextField(blank=True, null=True)
	published_on_dbz = models.CharField(max_length=75, blank=False, null=True)
	published_on_pf = models.CharField(max_length=75, blank=False, null=True)
	published_on_bayut = models.CharField(max_length=75, blank=False, null=True)
	

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
		self.agent_email = soup.agent_email.text
		self.agent_name = soup.agent_name.text
		self.agent_mobile = soup.agent_phone.text
		self.city = soup.city.text
		#converting type and subtype to dbz format
		category = soup.category.text
		type = soup.type.text
		if category == 'Residential for Rent':
			self.type = 'RP'
			if type == 'Apartment':
				self.subtype = 'AP'
			elif type == 'Villa':
				self.subtype = 'VI'
		elif category == 'Residential for Sale':
			self.type = 'SP'
			if type == 'Apartment':
				self.subtype = 'AP'
			elif type == 'Villa':
				self.subtype = 'VI'
		elif category == 'Commercial for Rent':
			self.type = 'RP'
			self.subtype = 'CO'
			if type == 'Office Space':
				self.commercialtype = 'OF'
			elif type == 'Retail':
				self.commercialtype = 'RE'
			elif type == 'Staff Accommodation':
				self.commercialtype = 'ST'
			elif type == 'Warehouse' or type == 'Factory':
				self.commercialtype = 'IN'
		elif category == 'Commercial for Sale':
			self.type = 'SP'
			self.subtype = 'CO'
			if type == 'Office Space':
				self.commercialtype = 'OF'
			elif type == 'Retail':
				self.commercialtype = 'RE'
			elif type == 'Staff Accommodation':
				self.commercialtype = 'ST'
			elif type == 'Warehouse' or type == 'Factory':
				self.commercialtype = 'IN'
		self.refno = soup.reference.text
		self.title = soup.title_en.text
		self.description = soup.description_en.text
		self.size = soup.sqft.text if soup.sqft else None
		self.price = soup.price.text
		if soup.bedroom:
			if soup.bedroom.text == 'studio':
				self.bedrooms = 0
			else:
				self.bedrooms = soup.bedroom.text
		#parse lastupdate and convert to datetime
		# self.feed_lastupdated = soup.lastupdated.text
		self.location = soup.community.text if soup.community else None
		self.building = soup.property.text if soup.property else None
		if soup.bathroom:
			self.bathrooms = soup.bathroom.text
		# if soup.amenities:
		# 	self.amenities = parse_dbz_amenities(soup.amenities.text)

		photos = soup.findAll(re.compile('photo_url'))
		if photos:
			self.photos = ''
			for key,photo in enumerate(photos):
				self.photos += photo.text.strip('\n\n')
				if (key+1) < len(photos):
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