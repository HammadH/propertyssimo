import requests
import datetime

from django.conf import settings

from bs4 import BeautifulSoup

from listings.models import Listing


def parse_platform_xml():
	# try:
	# 	response = requests.get(settings.DBZ_XML_LINK)
	# except Exception, e:
	# 	print e
	# 	return
	response = open('/home/dubizzle/ps.xml', 'r').read()
	### response.content if getting from request
	soup = BeautifulSoup(response)
	#################################
	listings = soup.find_all('refno')
	print "got %s listings" %len(listings)
	for refno_tag in listings:
		listing = refno_tag.parent
		print "processing %s" %refno_tag.text
		try:
			existing_listing = Listing.objects.get(refno=refno_tag.text)
			print "found existing %s" %refno_tag.text
			if existing_listing.feed_lastupdated == listing.lastupdated.text:
				print "%s hasn't been updated" %refno_tag.text
				continue
			else:
				print "%s has been updated" %refno_tag.text
				if listing.status.text == 'vacant':
					updated_listing = existing_listing.create_or_update_from_platform_dbz(listing)
					updated_listing.save()
					continue
				elif listing.status.text == 'deleted':
					existing_listing.delete()
					continue
		except Listing.DoesNotExist:
			if listing.status.text == 'vacant':
				new_listing = Listing().create_or_update_from_platform_dbz(listing)
				new_listing.created_at = datetime.datetime.now()
				new_listing.save()
				continue

def parse_dbz_xml():
	# try:
	# 	response = requests.get(settings.DBZ_XML_LINK)
	# except Exception, e:
	# 	print e
	# 	return
	response = open('/home/dubizzle/ps.xml', 'r').read()
	### response.content if getting from request
	soup = BeautifulSoup(response)
	#################################
	listings = soup.find_all('refno')
	print "got %s listings" %len(listings)
	for refno_tag in listings:
		listing = refno_tag.parent
		print "processing %s" %refno_tag.text
		try:
			existing_listing = Listing.objects.get(refno=refno_tag.text)
			print "found existing %s" %refno_tag.text
			if existing_listing.feed_lastupdated == listing.lastupdated.text:
				print "%s hasn't been updated" %refno_tag.text
				continue
			else:
				print "%s has been updated" %refno_tag.text
				if listing.status.text == 'vacant':
					updated_listing = existing_listing.create_or_update_from_dbz_xml(listing)
					updated_listing.published_on_dbz = 'True'
					updated_listing.save()
					continue
				elif listing.status.text == 'deleted':
					existing_listing.published_on_dbz = 'False'
					existing_listing.delete()
					continue
		except Listing.DoesNotExist:
			if listing.status.text == 'vacant':
				new_listing = Listing().create_or_update_from_dbz_xml(listing)
				new_listing.created_at = datetime.datetime.now()
				new_listing.published_on_dbz = 'True'
				new_listing.save()
				continue

def parse_pf_xml():
	#try:
	# 	response = requests.get(settings.PF_XML_LINK)
	# except Exception, e:
	# 	print e
	# 	return
	response = open('/home/dubizzle/pf.xml', 'r').read()
	soup = BeautifulSoup(response)
	listings = soup.find_all('reference')
	#### if listing not in xml; remove it ###
	### get all active listings from db, then parse all listings in xml,
	## the difference listings are the ones deleted from xml 
	listings_in_db = list(Listing.objects.filter(status=1))
	listings_in_xml = []

	print "got %s listings" %len(listings)
	for refno_tag in listings:
		listing = refno_tag.parent
		reference = refno_tag.text
		try:
			existing_listing = Listing.objects.get(refno=reference)
			print "found existing %s" %reference
			updated_listing = existing_listing.create_or_update_from_pf_xml(listing)
			updated_listing.published_on_pf = 'True'
			updated_listing.save()
			listings_in_xml.append(updated_listing)
			continue
		except Listing.DoesNotExist:
			print 'creating new listing: %s' %reference
			new_listing = Listing().create_or_update_from_pf_xml(listing)
			new_listing.created_at = datetime.datetime.now()
			new_listing.published_on_pf = 'True'
			new_listing.save()
			continue
	
	listings_to_delete = [listing for listing in listings_in_db if listing not in listings_in_xml]
	for listing in listings_to_delete:
		print "deleting %s" %listing.refno
		listing.published_on_pf = 'False'
		listing.delete()



