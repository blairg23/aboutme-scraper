#!/usr/bin/python
# -*- coding: utf-8 -*-
import data_load
import settings
import pickle
import os
import sys
import pandas
from datetime import datetime

class ScrapeSession:
	"""Create a scrape session."""
	
	def __init__(self):
		self.clear_memory = False
		self.current_term = None
		if '-cm' in sys.argv:
			self.clear_memory = True
			self.current_term = sys.argv[3]
		if '-mn' in sys.argv:
			self.current_term = sys.argv[3]
		self.search_list = []
		
		
	def general_scrape(self, search_key):
		"""Search for something, retrieve all the users found,
		   scrape user information and add completed to complete list."""
		
		os.system('clear')
		print('Preparing to scrape search key %s...' % search_key)
		with open('%s%s' % (settings.COMPLETED_PATH, settings.COMPLETED_USER_LIST), 'r') as f:
			temp_com_list = f.readlines()
			completed_list = []
			for name in temp_com_list:
				completed_list.append(name.strip())
		if self.clear_memory == False:
			with open('%s%s' % (settings.USER_LIST_DIR, settings.USER_LIST_LOG), 'r') as f:
				user_log = f.readlines()
				temp_log_list = []
				for user in user_log:
					temp_log_list.append(user.strip())
			if search_key in temp_log_list:
				for file_name in os.listdir(settings.USER_LIST_DIR):
					if search_key in file_name:
						name_file = file_name
				with open('%s%s' % (settings.USER_LIST_DIR, name_file), 'r') as f:
					temp_userids = f.readlines()
					userids = []
					for name in temp_userids:
						userids.append(name.strip())
			else:
				name_key = data_load.GetUsers(search_key)
				name_file = name_key.username_list_file
				if name_key.user_ids == None:
					return False
				else:
					userids = name_key.user_ids
		else:
			name_file = sys.argv[2]
			with open('%s%s' % (settings.USER_LIST_DIR, name_file), 'r') as f:
				temp_userids = f.readlines()
				userids = []
				for name in temp_userids:
					userids.append(name.strip())
		print("Scraping %d users." % len(userids))
		completed = []
		count = 0
		current_count = 0
		for user in userids:
			self.current_name = user
			if current_count > settings.CLEAR_MEMORY:
				print('Clearing memory')
				data_load.kill_webkit_server()
				os.execv(sys.executable, [sys.executable] + 
					[os.path.abspath(__file__),'-cm', name_file, search_key])
			os.system('clear')
			print("Currently scraping: %s (%d / %d)" % (user, count, len(userids)))
			if user in completed_list:
				print('User: %s was previously scraped already. Moving to next user.' % user)
				pass
			else:
				userdata = data_load.ScrapeUserData(user)
				if userdata.old == None:
					pass
				else:
					pickle.dump(userdata.user_data, open("%s%s.p" % (settings.USER_DATA_DIR, user), "w"))
					completed.append(user)
					with open('%s%s' % (settings.COMPLETED_PATH, settings.COMPLETED_USER_LIST), 'a') as f:
						f.write(user + '\n')
					current_count += 1
			os.system('clear')
			count += 1
		with open('%s%s' % (settings.COMPLETED_PATH, settings.COMPLETED_SEARCH_TERMS), 'a') as f:
			f.write(search_key + '\n')
		try:
			self.current_term = self.search_list[1]
			os.execv(sys.executable, [sys.executable] + [os.path.abspath(__file__), '-mn', name_file, self.current_term])
		except IndexError:
			data_load.kill_webkit_server()
			
	def get_mime_ext(self, file_name):
		"""Get the extension for file."""
		ext_begin_index = file_name.rfind('.')
		return file_name[ext_begin_index:]
		
	def format_for_pandas(self, file_name):
		"""Make sure txt column has correct name."""
		with open(file_name, 'r') as f:
			temp_data = f.readlines()
		if temp_data[0].strip() != 'name':
			with open(file_name, 'w') as f:
				temp_str = ''
				for name in temp_data:
					temp_str += name
				f.write('name\n' + temp_str)
			
	def load_lists(self):
		"""Load all search terms from files in settings.SEARCH_FILES.
		   Populate to self.search_list field."""
		list_files = []
		for list_file in settings.SEARCH_FILES:
			list_files.append(list_file)
		for search_file in list_files:
			mime_ext = self.get_mime_ext(search_file)
			temp_file_name = '%s%s' % (settings.SEARCH_LIST_DIR, search_file)
			if mime_ext == '.txt':
				self.format_for_pandas(temp_file_name)
			search_file = pandas.read_csv(temp_file_name)
			for name in search_file.name:
				self.search_list.append(name)
				
	def search_list_scrape(self):
		"""Search through and extract data from users found through
		   searches made from self.search_list terms."""
		self.load_lists()
		with open('%s%s' % (settings.COMPLETED_PATH, settings.COMPLETED_SEARCH_TERMS), 'r') as f:
			temp_comp_search = f.readlines()
			completed_list = []
			for term in temp_comp_search:
				completed_list.append(term.strip())
		if self.current_term is not None:
			current_index = self.search_list.index(self.current_term)
			leftover_list = self.search_list[current_index:]
		else:
			leftover_list = self.search_list
		for term in leftover_list:
			if term in completed_list:
				pass
			else:
				self.general_scrape(term)
				
					
			
	
a = ScrapeSession()
a.search_list_scrape()

