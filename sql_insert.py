import MySQLdb
import settings
import os
import pickle
import re

sql_queries = {
		'cdb_abs': "CREATE DATABASE aboutmedata;",
		'use_db' : "USE {0}".format(settings.MYSQL_DB_NAME),
		'ct_base': "CREATE TABLE {0} ({0}_id int not null auto_increment primary key, {0}_name varchar({1}) not null, unique({0}_name));",
		'bi_base': "CREATE TABLE {0} ({0}_id int not null auto_increment primary key, {0}_name LONGTEXT not null);",
		'ct_link': "CREATE TABLE user_{0} (user_id int not null, {0}_id int not null, foreign key (user_id) references user (user_id), foreign key ({0}_id) references {0} ({0}_id));",
		'i_base' : "INSERT INTO {0} ({0}_name) VALUES ('{1}');",
		'i_link' : "INSERT INTO user_{0} SELECT x.user_id, y.{0}_id FROM user x, {0} y WHERE x.user_name = '{1}' AND y.{0}_name = '{2}';",
}

tables = {
	'user': ['user', 120],
	'bio_html': ['bio_html'],
	'bio_text': ['bio_text'],
	'firstname': ['firstname', 120],
	'lastname': ['lastname', 120],
	'email': ['email', 120],
	'phone': ['phone', 120],
	'jobs': ['jobs', 120],
	'company': ['company', 120],
	'location': ['location', 120],
	'interests': ['interests', 120],
	'websites': ['websites', 120],
	'linkedin': ['linkedin', 120],
	'twitter': ['twitter', 120],
	'fb': ['fb', 120],
	'gplus': ['gplus', 120],
	'pinterest': ['pinterest', 120],
	'youtube': ['youtube', 120],
	'instagram': ['instagram', 120],
	'wordpress': ['wordpress', 120],
	'tumblr': ['tumblr', 120],
	'blogger': ['blogger', 120],
	'quora': ['quora', 120],
	'vimeo': ['vimeo', 120],
	'vine': ['vine', 120],
	'flickr': ['flickr', 120],
	'fitbit': ['fitbit', 120],
	'500px': ['500px', 120],
	'dribbble': ['dribbble', 120],
	'behance': ['behance', 120],
	'github': ['github', 120],
	'etsy': ['etsy', 120],
	'foursquare': ['foursquare', 120],
	'kickstarter': ['kickstarter', 120],
	'soundcloud': ['soundcloud', 120],
	'yelp': ['yelp', 120],
	'vk': ['vk', 120],
	'weibo': ['weibo', 120],
	'medium': ['medium', 120],
	'strava': ['strava', 120],
	'spotify': ['spotify', 120],
	'wikipedia': ['wikipedia', 120],
	'goodreads': ['goodreads', 120],
}

def create_tables(cursor):
	try:
		cursor.execute(sql_queries['bi_base'].format(tables['user'][0], tables['user'][1]))
	except:
		pass
	for key, value in tables.iteritems():
		if key == 'user':
			pass
		else:
			if key == 'bio_html' or key == 'bio_text':
				try:
					cursor.execute(sql_queries['bi_base'].format(tables[key][0]))
				except:
					pass
				try:
					#print(sql_queries['ct_link'].format(tables[key][0]))
					cursor.execute(sql_queries['ct_link'].format(tables[key][0]))
				except:
					pass
			else:
				try:
					cursor.execute(sql_queries['ct_base'].format(tables[key][0], tables[key][1]))
				except:
					pass
				try:
					cursor.execute(sql_queries['ct_link'].format(tables[key][0]))
				except:
					pass

def populate_user(cursor, user):
	if user == 'inserted_users':
		return False
	f = pickle.load(open('%s%s' % (settings.USER_DATA_DIR, user), 'rb'))
	temp_user = user
	user = user[:-2]
	cursor.execute(sql_queries['i_base'].format('user', user))
	for key, value in tables.iteritems():
		if key == 'user' or key == 'bio_text' or key == '\n':
			pass
		else:
			for x in f[key]:
				x = x.replace("'", "\\'")
				#print(sql_queries['i_base'].format(tables[key][0], x))
				try:
					cursor.execute(sql_queries['i_base'].format(tables[key][0], x))
				except:
					pass
			for x in f[key]:
				x = x.replace("'", "\\'")
				try:
					cursor.execute(sql_queries['i_link'].format(tables[key][0], user, x))
				except:
					pass
	with open('%s%s' % (settings.USER_DATA_DIR, settings.USER_DATA_POPULATED), 'a') as f:
		f.write(temp_user + '\n')

def populate_all(cursor):
	user_list = os.listdir(settings.USER_DATA_DIR)
	comp_user = []
	with open('%s%s' % (settings.USER_DATA_DIR, settings.USER_DATA_POPULATED), 'r') as f:
		temp_list = f.readlines()
		for user in temp_list:
			comp_user.append(user.strip())
	not_users = ['inserted_users.txt', 'inserted_users.txt~', 'inserted_users']
	print("Making insertions...")
	count = 0
	for user in user_list:
		if user in not_users:
			pass
		if user in comp_user:
			pass
		else:
			try:
				print("Inserting user: %s" % user)
				populate_user(cursor, user)
				count += 1
				comp_user.append(user.strip())
			except IndexError, EOF:
				print(user)
	print("Inserted: %d" % count)
	print("Total insertions: %d" % len(comp_user))
	
	

if len(settings.MYSQL_PORT) > 0:
	db = MySQLdb.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PWD, settings.MYSQL_DB_NAME, settings.MYSQL_PORT)
else:
	try:
		db = MySQLdb.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PWD, settings.MYSQL_DB_NAME)
	except:
			try:
				cur.execute(sql_queries['cdb_abs'])
			except:
				pass

cur = db.cursor()
cur.execute(sql_queries['use_db'])
create_tables(cur)
populate_all(cur)
db.commit()
