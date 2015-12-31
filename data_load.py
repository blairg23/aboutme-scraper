#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime
import store_re
import dryscrape
import settings
import time
import sys
import re
import os

def kill_webkit_server():
	os.system('killall -9 webkit_server')
	os.system('killall -9 Xvfb')

class GetUsers:
	"""Get username list based on search keyword."""
	
	def __init__(self, search_keyword):
		dryscrape.start_xvfb()
		self.search_keyword = search_keyword
		self.sess = dryscrape.Session(base_url='https://about.me')
	
		# Disable image loading
		self.sess.set_attribute('auto_load_images', settings.IMG_LOAD)
		self.username_list_file = ''
		self.user_ids = None
	
		# Get usernames
		self.extract_usernames()
	
	def scroll_down(self, st):
		"""Scroll to bottom of page to load data."""
		print('Scrolling down... %s results loaded.' % str(st * 65))
		try:
			self.sess.exec_script('window.scrollTo(0,document.body.scrollHeight);')
			return True
		except:
			return False
	
	def check_reach_end(self):
		"""Check to see if there is no more data to load
		or if search returns empty."""
		temp_soup = BeautifulSoup(self.sess.body().encode('utf8'))
		endpoint_str = 'There are no'
		if endpoint_str in temp_soup.find('p', {'class': 'search-number'}).text:
			return True
		else:
			return False

	def get_raw_html(self):
		"""Load up the entire page contents and return HTML."""
		self.sess.visit('/search')
		time.sleep(settings.INPUT_SEARCH)
		print('Searching for %s on about.me...' % self.search_keyword)
		search_field = self.sess.at_xpath("//input[@class='input search-main-field']")
		time.sleep(settings.INPUT_SEARCH)
		search_field.set(self.search_keyword)
		time.sleep(settings.INPUT_SEARCH)
		search_click = self.sess.at_xpath("//button[@class='button submitbutton glyph-search glyph-center']")
		time.sleep(settings.INPUT_SEARCH)
		search_click.click()
		time.sleep(settings.CLICK_SEARCH)
		print('Loading page for keyword %s (this may take a few minutes)...' % self.search_keyword)
		page_load_status = False
		error_tries = 0
		scroll_times = 0
		while not page_load_status:
			if error_tries > settings.CONN_ERROR_TRIES:
				if scroll_times > 0:
					with open("%s%s" % (settings.SEARCH_LIST_DIR, 'incomplete.txt'), 'a') as f:
						f.write(self.search_keyword)
				break
			scroll = self.scroll_down(scroll_times)
			if scroll == True:
				scroll_times += 1
			time.sleep(settings.SCROLL_SPEED)
			try:
				raw_html = self.sess.body().encode('utf8')
			except:
				pass
			try:
				page_loaded = self.check_reach_end()
				if page_loaded:
					page_load_status = True
					raw_html = self.sess.body().encode('utf8')
					print('Extracted raw html for keyword %s.' % self.search_keyword)
			except:
				print('Connection Error! Retrying in 3 seconds...')
				error_tries += 1
				time.sleep(settings.RETRY_SLEEP)
		if page_load_status:
			return raw_html
		else:
			print('Please check your connection.')
			if scroll_times > 0:
				return raw_html
			else:
				return False

	def extract_usernames(self):
		"""Extract usernames for search keyword, store in temp storage."""
		with open('%s%s' % (settings.USER_LIST_DIR, settings.USER_LIST_LOG), 'r') as f:
			user_log = f.readlines()
			temp_log_list = []
			for user in user_log:
				temp_log_list.append(user.strip())
		if self.search_keyword in temp_log_list:
			return True
		else:
			search_raw_html = self.get_raw_html()
			if search_raw_html:
				print('Extracting usernames for %s...' % self.search_keyword)
				html_souped = BeautifulSoup(search_raw_html)
				userid_raw = html_souped.find_all('a', {'class': 'thumb_link'})
				userids = []
				for user in userid_raw:
					userids.append(user['href'][1:])
				print('Usernames extracted. Putting in temp storage.')
				username_file = '%s_users.txt' % (self.search_keyword)
				self.username_list_file = username_file
				self.user_ids = userids
				with open('%s%s' % (settings.USER_LIST_DIR, username_file), 'a') as f:
					for user in userids:
						f.write(user + '\n')
				with open('%s%s' % (settings.USER_LIST_DIR, settings.USER_LIST_LOG), 'r') as f:
					user_log = f.readlines()
					temp_log_list = []
					for user in user_log:
						temp_log_list.append(user)
					if self.search_keyword not in temp_log_list:
						with open('%s%s' % (settings.USER_LIST_DIR, settings.USER_LIST_LOG), 'a') as f:
							f.write(self.search_keyword + '\n')


class ScrapeUserData:
	"""Scrape data from username url."""
	
	def __init__(self, username):
		dryscrape.start_xvfb()
		self.username = username
		self.sess = dryscrape.Session(base_url='https://about.me/')
		self.user_data = {
			'firstname': [],
			'lastname': [],
			'email': [],
			'phone': [],
			'jobs': [],
			'company': [],
			'websites': [],
			'linkedin': [],
			'twitter': [],
			'fb': [],
			'gplus': [],
			'pinterest': [],
			'youtube': [],
			'instagram': [],
			'wordpress': [],
			'tumblr': [],
			'blogger': [],
			'quora': [],
			'vimeo': [],
			'vine': [],
			'flickr': [],
			'fitbit': [],
			'500px': [],
			'dribbble': [],
			'medium': [],
			'behance': [],
			'github': [],
			'etsy': [],
			'foursquare': [],
			'kickstarter': [],
			'soundcloud': [],
			'yelp': [],
			'vk': [],
			'strava': [],
			'spotify': [],
			'wikipedia': [],
			'goodreads': [],
			'city': [],
			'state': [],
			'country': [],
			'location': [],
			'weibo': [],
			'interests': [],
			'bio_html': [],
			'bio_text': [],
		}
	
		self.old = False
		self.souped_html = BeautifulSoup(self.get_raw_html())
		self.set_old_or_new()
		if self.old == None:
			return None
		else:
			print("'%s' ready to be scraped." % self.username)
			time.sleep(0.5)
			self.get_all_data()
	
	def get_raw_html(self):
		self.sess.visit('/%s' % self.username)
		time.sleep(1.5)
		raw_html = self.sess.body().encode('utf8')
		return raw_html
	
	def set_old_or_new(self):
		tries = settings.CONN_ERROR_TRIES
		while tries:
			try:
				if len(self.souped_html.find('h1', {'class': 'name'})) > 1:
					self.old = True
				else:
					self.old = False
				return True
			except TypeError:
				tries -= 1
		self.old = None
		return False
	
	def get_bio(self):
		if self.old:
			try:
				bio = self.souped_html.find(
					'div', {'class': 'bio-container'})
				self.user_data['bio_html'].append(bio.text.encode('ascii', 'ignore').strip())
				bio_p = bio.find_all('p')
				bio_text = ''
				for p in bio_p:
					temp_str = p.text.encode('ascii', 'ignore').strip()
					bio_text += temp_str				
				self.user_data['bio_text'] = bio_text.encode('ascii', 'ignore').strip()
			except (AttributeError, TypeError):
				return False
		else:	
			try:
				bio = self.souped_html.find(
					'section', {'class': 'bio-container'})
				self.user_data['bio_html'].append(bio.text.encode('ascii', 'ignore').strip())
				bio_p = bio.find_all('p')
				bio_text = ''
				for p in bio_p:
					temp_str = p.text.encode('ascii', 'ignore').strip()
					bio_text += temp_str
				self.user_data['bio_text'] = bio_text.encode('ascii', 'ignore').strip()
			except (AttributeError, TypeError):
				return False
						
	
	def get_firstname(self):
		if self.old:
			try:
				fname = self.souped_html.find(
					'span', {'class': 'first_name-container'}).text
				self.user_data['firstname'].append(fname.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				fname = self.souped_html.find('h1', {'class': 'name'}).text.split()[0]
				self.user_data['firstname'].append(fname.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_lastname(self):
		if self.old:
			try:
				lname = self.souped_html.find(
					'span', {'class': 'last_name-container'}).text
				self.user_data['lastname'].append(lname.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				lname = self.souped_html.find('h1', {'class': 'name'}).text.split()[1]
				self.user_data['lastname'].append(lname.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_email(self):
		if len(self.user_data['bio_html']) == 0:
			self.get_bio()
		try:
			email_whtml_s = re.findall(store_re.email_expr, 
				self.user_data['bio_html'][0].encode('ascii', 'ignore').strip())
			emails = []
			for email in email_whtml_s:
				emails.append(email)
			for email in emails:
				self.user_data['email'].append(email.encode('ascii', 'ignore').strip())
		except KeyError:
			return False
	
	def get_phone(self):
		if len(self.user_data['bio_html']):
			self.get_bio()
		if self.old:
			try:
				phone_num = self.souped_html.find(
					'ul', {'class': 'list phone glyph-phone'}).text
				self.user_data['phone'].append(phone_num.encode('ascii', 'ignore').strip())
				phone_match = re.findall(store_re.phone_expr, str(self.user_data['bio_html'][0]))
				if len(phone_match) > 0:
					for num in phone_match:
						self.user_data['phone'].append(num.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			phone_match = re.findall(store_re.phone_expr, str(self.user_data['bio_html'][0]))
			if len(phone_match) > 0:
				for num in phone_match:
					self.user_data['phone'].append(num.encode('ascii', 'ignore').strip())
			else:
				return False
	
	def get_job(self):
		if self.old:
			try:
				jobs = self.souped_html.find(
					'ul', {'class': 'list jobs glyph-building'}).text
				self.user_data['jobs'].append(jobs.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				jobs = self.souped_html.find(
					'h2', {'class': 'headline'}).find_all('span', {
						'class': 'role'})
				job_list = []
				for job in jobs:
					temp_job = job.text.encode('ascii', 'ignore').strip()
					if temp_job in self.user_data['jobs']:
						pass
					else:
						job_list.append(temp_job)
				for job in job_list:
					self.user_data['jobs'].append(job.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_company(self):
		if self.old:
			return False
		else:
			try:
				company = self.souped_html.find(
					'li', {'class': 'meta-section jobs'}).find('li', {'class': 'meta-item'}).text
				company = company.encode('ascii', 'ignore').strip().strip()
				self.user_data['company'].append(company.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
				
	def get_location(self):
		if self.old:
			# find city and state by class 'group'
			try:
				city = self.souped_html.find('span', {'class': 'city'}).text.encode('ascii', 'ignore').strip()
				state = self.souped_html.find('span', {'class': 'state'}).text.encode('ascii', 'ignore').strip()
				country = self.souped_html.find('li', {'class': 'state'}).text.encode('ascii', 'ignore').strip()
				if len(city) > 0:
					self.user_data['city'].append(city.encode('ascii', 'ignore').strip())
				if len(state) > 0:
					self.user_data['state'].append(state.encode('ascii', 'ignore').strip())
				if len(country) > 0:
					self.user_data['country'].append(country.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				try:
					cities = self.souped_html.find(
						'ul', {'class': 'list locations glyph-locations'}).find_all('li')
					place_list = []
					for place in cities:
						temp_place = str(place.text).strip()
						if temp_place in self.user_data['locations']:
							pass
						else:
							place_list.append(temp_place)
					for place in place_list:
						self.user_data['location'].append(place.encode('ascii', 'ignore').strip())
				except (AttributeError, TypeError):
					pass
			try:
				cities = self.souped_html.find(
					'ul', {'class': 'list locations glyph-location'}).find_all('li')
				place_list = []
				for place in cities:
					temp_place = place.text.encode('ascii', 'ignore').strip()
					place_list.append(temp_place)
				for place in place_list:
					self.user_data['location'].append(place.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				city_state = str(self.souped_html.find('h2', {'class': 'headline'}).text)
				extract_cs = re.search('(?<=\sin\s)(\w+\s*)+,\s(\w+\s*)+', city_state)
				city_state = extract_cs.group(0)
				self.user_data['location'] = city_state
				city_string = re.search('(\w+\s*)+[^,]', city_state)
				city = city_string.group(0)
				state_string = re.search('(?<=,\s)(\w+\s*)+', city_state)
				state = state_string.group(0)
				self.user_data['city'].append(city.encode('ascii', 'ignore').strip())
				self.user_data['state'].append(state.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_interests(self):
		if self.old:
			try:
				interests = self.souped_html.find(
					'div', {'class': 'tags-container'}).find_all('li')
				interest_list = []
				for interest in interests:
					temp_interest = interest.text.encode('ascii', 'ignore').strip()
					temp_interest = temp_interest.strip()
					if temp_interest in self.user_data['interests']:
						pass
					else:
						interest_list.append(temp_interest)
				for interest in interest_list:
					self.user_data['interests'].append(interest.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				pass
			try:
				interests = self.souped_html.find(
					'div', {'class': 'interests-container'}).find_all('li')
				interest_list = []
				for interest in interests:
					temp_interest = interest.text.encode('ascii', 'ignore').strip()
					temp_interest = temp_interest.strip()
					if temp_interest in self.user_data['interests']:
						pass
					else:
						interest_list.append(temp_interest)
				for interest in interest_list:
					self.user_data['interests'].append(interest.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				interests = self.souped_html.find_all('li', {'class': 'interest'})
				interest_list = []
				for interest in interests:
					temp_interest = interest.text.encode('ascii', 'ignore').strip()
					temp_interest = temp_interest[1:]
					if temp_interest in self.user_data['interests']:
						pass
					else:
						interest_list.append(temp_interest)
				for interest in interest_list:
					self.user_data['interests'].append(interest.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_websites(self):
		if len(self.user_data['bio_html']) == 0:
			self.get_bio()
		if self.old:
			try:
				sites = self.souped_html.find(
					'ul', {'class': 'links clearfix'}).find_all('a', {'class': 'website'})
				site_list = []
				for site in sites:
					temp_site = site['href'].encode('ascii', 'ignore').strip()
					if temp_site in self.user_data['websites']:
						pass
					else:
						site_list.append(temp_site)
				for site in site_list:
					self.user_data['websites'].append(site.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
			try:
				bio_soup = BeautifulSoup(str(self.user_data['bio_html'][0]))
				sites = bio_soup.find_all('a')
				site_list = []
				for site in sites:
					temp_site = str(site['href']).strip()
					if temp_site in self.user_data['websites']:
						pass
					else:
						site_list.append(temp_site)
				site_match = re.findall(store_re.website_expr, str(self.user_data['bio_html'][0]))
				for site in site_match:
					temp_site = str(site).strip()
					site_list.append(temp_site)
				for site in site_list:
					self.user_data['websites'].append(site.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				spotlight_site = self.souped_html.find(
					'section', {'class': 'spotlight-container'}).find('a')['href']
				self.user_data['websites'].append(spotlight_site.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
			try:
				bio_soup = BeautifulSoup(str(self.user_data['bio_html'][0]))
				sites = bio_soup.find_all('a')
				site_list = []
				for site in sites:
					temp_site = str(site['href']).strip()
					if temp_site in self.user_data['websites']:
						pass
					else:
						site_list.append(temp_site)
				site_match = re.findall(store_re.website_expr, str(self.user_data['bio_html'][0]))
				for site in site_match:
					temp_site = str(site).strip()
					site_list.append(temp_site)
				for site in site_list:
					self.user_data['websites'].append(site.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_linkedin(self):
		if self.old:
			try:
				linkedin = self.souped_html.find(
					'a', {'class': 'icon linkedin'})['href']
				self.user_data['linkedin'].append(linkedin.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				linkedin = self.souped_html.find(
					'a', {'class': 'app linkedin glyph-center glyph-linkedin-circle'})['href']
				self.user_data['linkedin'].append(linkedin.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_twitter(self):
		if self.old:
			try:
				twitter = self.souped_html.find(
					'a', {'class': 'icon twitter'})['href']
				self.user_data['twitter'].append(twitter.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				twitter = self.souped_html.find(
					'a', {'class': 'app twitter glyph-center glyph-twitter-circle'})['href']
				self.user_data['twitter'].append(twitter.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_fb(self):
		if self.old:
			try:
				fb = self.souped_html.find('a',
										   {'class': 'icon facebook'})['href']
				self.user_data['fb'].append(fb.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				fb = self.souped_html.find(
					'a', {'class': 'app facebook glyph-center glyph-facebook-circle'})['href']
				self.user_data['fb'].append(fb.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_gplus(self):
		if self.old:
			try:
				gplus = self.souped_html.find(
					'a', {'class': 'icon googleplus'})['href']
				self.user_data['gplus'].append(gplus.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				gplus = self.souped_html.find(
					'a', {'class': 'app googleplus glyph-center glyph-gplus-circle'})['href']
				self.user_data['gplus'].append(gplus.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_pinterest(self):
		if self.old:
			try:
				pinterest = self.souped_html.find(
					'a', {'class': 'icon pinterest'})['href']
				self.user_data['pinterest'].append(pinterest.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				pinterest = self.souped_html.find(
					'a', {'class': 'app pinterest glyph-center glyph-pinterest-circle'})['href']
				self.user_data['pinterest'].append(pinterest.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_youtube(self):
		if self.old:
			try:
				youtube = self.souped_html.find(
					'a', {'class': 'icon youtube'})['href']
				self.user_data['youtube'].append(youtube.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				youtube = self.souped_html.find(
					'a', {'class': 'app youtube glyph-center glyph-youtube-circle'})['href']
				self.user_data['youtube'].append(youtube.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_instagram(self):
		if self.old:
			try:
				instagram = self.souped_html.find(
					'a', {'class': 'icon instagram'})['href']
				self.user_data['instagram'].append(instagram.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				instagram = self.souped_html.find(
					'a', {'class': 'app instagram glyph-center glyph-instagram-circle'})['href']
				self.user_data['instagram'].append(instagram.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_wordpress(self):
		if self.old:
			try:
				wordpress = self.souped_html.find(
					'a', {'class': 'icon wordpress'})['href']
				self.user_data['wordpress'].append(wordpress.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				wordpress = self.souped_html.find(
					'a', {'class': 'app wordpress glyph-center glyph-wordpress-circle'})['href']
				self.user_data['wordpress'].append(wordpress.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_tumblr(self):
		if self.old:
			try:
				tumblr = self.souped_html.find(
					'a', {'class': 'icon tumblr'})['href']
				self.user_data['tumblr'].append(tumblr.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				tumblr = self.souped_html.find(
					'a', {'class': 'app tumblr glyph-center glyph-tumblr-circle'})['href']
				self.user_data['tumblr'].append(tumblr.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_blogger(self):
		if self.old:
			try:
				blogger = self.souped_html.find(
					'a', {'class': 'icon blogger'})['href']
				self.user_data['blogger'].append(blogger.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				blogger = self.souped_html.find(
					'a', {'class': 'app blogger glyph-center glyph-blogger-circle'})['href']
				self.user_data['blogger'].append(blogger.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_quora(self):
		if self.old:
			try:
				quora = self.souped_html.find(
					'a', {'class': 'icon quora'})['href']
				self.user_data['quora'].append(quora.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				quora = self.souped_html.find(
					'a', {'class': 'app quora glyph-center glyph-quora-circle'})['href']
				self.user_data['quora'].append(quora.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_vimeo(self):
		if self.old:
			try:
				vimeo = self.souped_html.find(
					'a', {'class': 'icon vimeo'})['href']
				self.user_data['vimeo'].append(vimeo.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				vimeo = self.souped_html.find(
					'a', {'class': 'app vimeo glyph-center glyph-vimeo-circle'})['href']
				self.user_data['vimeo'].append(vimeo.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_vine(self):
		if self.old:
			try:
				vine = self.souped_html.find(
					'a', {'class': 'icon vine'})['href']
				self.user_data['vine'].append(vine.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				vine = self.souped_html.find(
					'a', {'class': 'app vine glyph-center glyph-vine-circle'})['href']
				self.user_data['vine'].append(vine.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_flickr(self):
		if self.old:
			try:
				flickr = self.souped_html.find(
					'a', {'class': 'icon flickr'})['href']
				self.user_data['flickr'].append(flickr.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				flickr = self.souped_html.find(
					'a', {'class': 'app flickr glyph-center glyph-flickr-circle'})['href']
				self.user_data['flickr'].append(flickr.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_fitbit(self):
		if self.old:
			try:
				fitbit = self.souped_html.find(
					'a', {'class': 'icon fitbit'})['href']
				self.user_data['fitbit'].append(fitbit.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				fitbit = self.souped_html.find(
					'a', {'class': 'app fitbit glyph-center glyph-fitbit-circle'})['href']
				self.user_data['fitbit'].append(fitbit.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_500px(self):
		if self.old:
			try:
				px500 = self.souped_html.find(
					'a', {'class': 'icon px500'})['href']
				self.user_data['500px'].append(px500.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				px500 = self.souped_html.find(
					'a', {'class': 'app px500 glyph-center glyph-px500-circle'})['href']
				self.user_data['500px'].append(px500.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_dribbble(self):
		if self.old:
			try:
				dribbble = self.souped_html.find(
					'a', {'class': 'icon dribbble'})['href']
				self.user_data['dribbble'].append(dribbble.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				dribbble = self.souped_html.find(
					'a', {'class': 'app dribbble glyph-center glyph-dribbble-circle'})['href']
				self.user_data['dribbble'].append(dribbble.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_behance(self):
		if self.old:
			try:
				behance = self.souped_html.find(
					'a', {'class': 'icon behance'})['href']
				self.user_data['behance'].append(behance.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				behance = self.souped_html.find(
					'a', {'class': 'app behance glyph-center glyph-behance-circle'})['href']
				self.user_data['behance'].append(behance.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_github(self):
		if self.old:
			try:
				github = self.souped_html.find(
					'a', {'class': 'icon github'})['href']
				self.user_data['github'].append(github.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				github = self.souped_html.find(
					'a', {'class': 'app github glyph-center glyph-github-circle'})['href']
				self.user_data['github'].append(github.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_etsy(self):
		if self.old:
			try:
				etsy = self.souped_html.find(
					'a', {'class': 'icon etsy'})['href']
				self.user_data['etsy'].append(etsy.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				etsy = self.souped_html.find(
					'a', {'class': 'app etsy glyph-center glyph-etsy-circle'})['href']
				self.user_data['etsy'].append(etsy.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_foursquare(self):
		if self.old:
			try:
				foursquare = self.souped_html.find(
					'a', {'class': 'icon foursquare'})['href']
				self.user_data['foursquare'].append(foursquare.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				foursquare = self.souped_html.find(
					'a', {'class': 'app foursquare glyph-center glyph-foursquare-circle'})['href']
				self.user_data['foursquare'].append(foursquare.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_kickstarter(self):
		if self.old:
			try:
				kickstarter = self.souped_html.find(
					'a', {'class': 'icon kickstarter'})['href']
				self.user_data['kickstarter'].append(kickstarter.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				kickstarter = self.souped_html.find(
					'a', {'class': 'app kickstarter glyph-center glyph-kickstarter-circle'})['href']
				self.user_data['kickstarter'].append(kickstarter.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_soundcloud(self):
		if self.old:
			try:
				soundcloud = self.souped_html.find(
					'a', {'class': 'icon soundcloud'})['href']
				self.user_data['soundcloud'].append(soundcloud.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				soundcloud = self.souped_html.find(
					'a', {'class': 'app soundcloud glyph-center glyph-soundcloud-circle'})['href']
				self.user_data['soundcloud'].append(soundcloud.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_yelp(self):
		if self.old:
			try:
				yelp = self.souped_html.find(
					'a', {'class': 'icon yelp'})['href']
				self.user_data['yelp'].append(yelp.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				yelp = self.souped_html.find(
					'a', {'class': 'app yelp glyph-center glyph-yelp-circle'})['href']
				self.user_data['yelp'].append(yelp.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_vk(self):
		if self.old:
			try:
				vk = self.souped_html.find('a', {'class': 'icon vk'
												 })['href']
				self.user_data['vk'].append(vk.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				vk = self.souped_html.find(
					'a', {'class': 'app vk glyph-center glyph-vk-circle'})['href']
				self.user_data['vk'].append(vk.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_weibo(self):
		if self.old:
			try:
				weibo = self.souped_html.find(
					'a', {'class': 'icon weibo'})['href']
				self.user_data['weibo'].append(weibo.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				weibo = self.souped_html.find(
					'a', {'class': 'app weibo glyph-center glyph-weibo-circle'})['href']
				self.user_data['weibo'].append(weibo.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_medium(self):
		if self.old:
			try:
				medium = self.souped_html.find(
					'a', {'class': 'icon medium'})['href']
				self.user_data['medium'].append(medium.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				medium = self.souped_html.find(
					'a', {'class': 'app medium glyph-center glyph-medium-circle'})['href']
				self.user_data['medium'].append(medium.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_strava(self):
		if self.old:
			try:
				strava = self.souped_html.find(
					'a', {'class': 'icon strava'})['href']
				self.user_data['strava'].append(strava.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				strava = self.souped_html.find(
					'a', {'class': 'app strava glyph-center glyph-strava-circle'})['href']
				self.user_data['strava'].append(strava.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_spotify(self):
		if self.old:
			try:
				spotify = self.souped_html.find(
					'a', {'class': 'icon spotify'})['href']
				self.user_data['spotify'].append(spotify.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				spotify = self.souped_html.find(
					'a', {'class': 'app spotify glyph-center glyph-spotify-circle'})['href']
				self.user_data['spotify'].append(spotify.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_wikipedia(self):
		if self.old:
			try:
				wikipedia = self.souped_html.find(
					'a', {'class': 'icon wikipedia'})['href']
				self.user_data['wikipedia'].append(wikipedia.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				wikipedia = self.souped_html.find(
					'a', {'class': 'app wikipedia glyph-center glyph-wikipedia-circle'})['href']
				self.user_data['wikipedia'].append(wikipedia.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
	
	def get_goodreads(self):
		if self.old:
			try:
				goodreads = self.souped_html.find(
					'a', {'class': 'icon goodreads'})['href']
				self.user_data['goodreads'].append(goodreads.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
		else:
			try:
				goodreads = self.souped_html.find(
					'a', {'class': 'app goodreads glyph-center glyph-goodreads-circle'})['href']
				self.user_data['goodreads'].append(goodreads.encode('ascii', 'ignore').strip())
			except (AttributeError, TypeError):
				return False
				
	def get_all_data(self):
		time.sleep(1)
		print("Scraping data from user: %s" % self.username)
		if settings.TO_SCRAPE['bio']:
			self.get_bio()
		if settings.TO_SCRAPE['firstname']:
			self.get_firstname()
		if settings.TO_SCRAPE['lastname']:
			self.get_lastname()
		if settings.TO_SCRAPE['email']:
			self.get_email()
		if settings.TO_SCRAPE['phone']:
			self.get_phone()
		if settings.TO_SCRAPE['jobs']:
			self.get_job()
		if settings.TO_SCRAPE['company']:
			self.get_company()
		if settings.TO_SCRAPE['location']:
			self.get_location()
		if settings.TO_SCRAPE['interests']:
			self.get_interests()
		if settings.TO_SCRAPE['websites']:
			self.get_websites()
		if settings.TO_SCRAPE['linkedin']:
			self.get_linkedin()
		if settings.TO_SCRAPE['twitter']:
			self.get_twitter()
		if settings.TO_SCRAPE['fb']:
			self.get_fb()
		if settings.TO_SCRAPE['gplus']:
			self.get_gplus()
		if settings.TO_SCRAPE['pinterest']:
			self.get_pinterest()
		if settings.TO_SCRAPE['youtube']:
			self.get_youtube()
		if settings.TO_SCRAPE['instagram']:
			self.get_instagram()
		if settings.TO_SCRAPE['wordpress']:
			self.get_wordpress()
		if settings.TO_SCRAPE['tumblr']:
			self.get_tumblr()
		if settings.TO_SCRAPE['blogger']:
			self.get_blogger()
		if settings.TO_SCRAPE['quora']:
			self.get_quora()
		if settings.TO_SCRAPE['vimeo']:
			self.get_vimeo()
		if settings.TO_SCRAPE['vine']:
			self.get_vine()
		if settings.TO_SCRAPE['flickr']:
			self.get_flickr()
		if settings.TO_SCRAPE['fitbit']:
			self.get_fitbit()
		if settings.TO_SCRAPE['500px']:
			self.get_500px()
		if settings.TO_SCRAPE['dribbble']:
			self.get_dribbble()
		if settings.TO_SCRAPE['behance']:
			self.get_behance()
		if settings.TO_SCRAPE['github']:
			self.get_github()
		if settings.TO_SCRAPE['etsy']:
			self.get_etsy()
		if settings.TO_SCRAPE['foursquare']:
			self.get_foursquare()
		if settings.TO_SCRAPE['kickstarter']:
			self.get_kickstarter()
		if settings.TO_SCRAPE['soundcloud']:
			self.get_soundcloud()
		if settings.TO_SCRAPE['yelp']:
			self.get_yelp()
		if settings.TO_SCRAPE['vk']:
			self.get_vk()
		if settings.TO_SCRAPE['weibo']:
			self.get_weibo()
		if settings.TO_SCRAPE['medium']:
			self.get_medium()
		if settings.TO_SCRAPE['strava']:
			self.get_strava()
		if settings.TO_SCRAPE['spotify']:
			self.get_spotify()
		if settings.TO_SCRAPE['wikipedia']:
			self.get_wikipedia()
		if settings.TO_SCRAPE['goodreads']:
			self.get_goodreads()
		
