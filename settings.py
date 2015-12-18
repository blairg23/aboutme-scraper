#Set scroll down speed to get next set of data
SCROLL_SPEED = 0.01

#Number of times to try loading page before connection error
CONN_ERROR_TRIES = 5

#Sleep settings
INPUT_SEARCH = 2.5
CLICK_SEARCH = 5
RETRY_SLEEP = 3

#Set image load options
IMG_LOAD = False

#Search lists containing keywords to be searched
#Applicable only if LIST_OR_NOT is True
SEARCH_LIST_DIR = 'search_lists/to_scrape/'
SEARCH_FILES = (
	'names.txt',
)

#Name and filepath of list of users and search terms already scraped
COMPLETED_PATH = 'search_lists/completed/'
COMPLETED_USER_LIST = 'users/comp_users.txt'
COMPLETED_SEARCH_TERMS = 'search_terms/comp_search_terms.txt'

#File for pickle files stored for users already scraped
USER_DATA_DIR = 'user_data/'

#Userlist directory and log
USER_LIST_DIR = 'user_list/'
USER_LIST_LOG = 'log.txt'

#Clear memory
CLEAR_MEMORY = 35 #Suggested 35 per 8 gigs of ram (eg. 35 at 8gigs, 70 at 16gigs)

#Fields to Scrape
TO_SCRAPE = {
	'bio': True,
	'firstname': True,
	'lastname': True,
	'email': True,
	'phone': True,
	'jobs': True,
	'company': True,
	'location': True,
	'interests': True,
	'websites': True,
	'linkedin': True,
	'twitter': True,
	'fb': True,
	'gplus': True,
	'pinterest': True,
	'youtube': True,
	'instagram': True,
	'wordpress': True,
	'tumblr': True,
	'blogger': True,
	'quora': True,
	'vimeo': True,
	'vine': True,
	'flickr': True,
	'fitbit': True,
	'500px': True,
	'dribbble': True,
	'behance': True,
	'github': True,
	'etsy': True,
	'foursquare': True,
	'kickstarter': True,
	'soundcloud': True,
	'yelp': True,
	'vk': True,
	'weibo': True,
	'medium': True,
	'strava': True,
	'spotify': True,
	'wikipedia': True,
	'goodreads': True,
}


#MySQL Settings
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PWD = 'password'
MYSQL_DB_NAME = 'aboutmedata'
MYSQL_PORT = ''

