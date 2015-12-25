import MySQLdb
import settings
import os
import pickle
import re

sql_queries = {
		'cdb_abs': "CREATE DATABASE aboutmedata;",
		'use_db' : "USE {0}".format(settings.MYSQL_DB_NAME),
		'ct_base': "CREATE TABLE {0} ({0}_id int not null auto_increment primary key, {0}_name varchar({1}) not null);",
		'bi_base': "CREATE TABLE {0} ({0}_id int not null auto_increment primary key, {0}_name LONGTEXT not null);",
		'ct_link': "CREATE TABLE user_{0} (user_id int not null, {0}_id int not null, foreign key (user_id) references user (user_id), foreign key ({0}_id) references {0} ({0}_id));",
		'i_base' : "INSERT INTO {0} ({0}_name) VALUES ('{1}');",
		'i_link' : "INSERT INTO user_{0} SELECT x.user_id, y.{0}_id FROM user x, {0} y WHERE x.user_name = '{1}' AND y.{0}_name = '{2}';",
}

tables = {
	'user': ['user', 80],
	'bio_html': ['bio_html'],
	'bio_text': ['bio_text'],
	'firstname': ['firstname', 80],
	'lastname': ['lastname', 80],
	'email': ['email', 80],
	'phone': ['phone', 80],
	'jobs': ['jobs', 80],
	'company': ['company', 80],
	'location': ['location', 80],
	'interests': ['interests', 80],
	'websites': ['websites', 80],
	'linkedin': ['linkedin', 80],
	'twitter': ['twitter', 80],
	'fb': ['fb', 80],
	'gplus': ['gplus', 80],
	'pinterest': ['pinterest', 80],
	'youtube': ['youtube', 80],
	'instagram': ['instagram', 80],
	'wordpress': ['wordpress', 80],
	'tumblr': ['tumblr', 80],
	'blogger': ['blogger', 80],
	'quora': ['quora', 80],
	'vimeo': ['vimeo', 80],
	'vine': ['vine', 80],
	'flickr': ['flickr', 80],
	'fitbit': ['fitbit', 80],
	'500px': ['500px', 80],
	'dribbble': ['dribbble', 80],
	'behance': ['behance', 80],
	'github': ['github', 80],
	'etsy': ['etsy', 80],
	'foursquare': ['foursquare', 80],
	'kickstarter': ['kickstarter', 80],
	'soundcloud': ['soundcloud', 80],
	'yelp': ['yelp', 80],
	'vk': ['vk', 80],
	'weibo': ['weibo', 80],
	'medium': ['medium', 80],
	'strava': ['strava', 80],
	'spotify': ['spotify', 80],
	'wikipedia': ['wikipedia', 80],
	'goodreads': ['goodreads', 80],
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
					print(sql_queries['ct_link'].format(tables[key][0]))
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

key_errors = ['user', 'bio_text', '\n']
def populate_user(cursor, user):
	f = pickle.load(open('%s%s' % (settings.USER_DATA_DIR, user), 'r'))
	user_re = re.search('[\w.]+[^.p]', user)
	user = user_re.group(0)
	cursor.execute(sql_queries['i_base'].format('user', user))
	for key, value in tables.iteritems():
		if key in key_errors:
			pass
		else:
			for x in f[key]:
				x = x.replace("'", "\\'")
				print(sql_queries['i_base'].format(tables[key][0], x))
				cursor.execute(sql_queries['i_base'].format(tables[key][0], x))
				print(sql_queries['i_link'].format(tables[key][0], user, x))
				cursor.execute(sql_queries['i_link'].format(tables[key][0], user, x))

def populate_all(cursor):
	user_list = os.listdir(settings.USER_DATA_DIR)
	for user in user_list:
		populate_user(cursor, user)
	

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
