# aboutme-scraper
Python web scraper for about.me profiles. Adds collected profiles to MySQL database.

# Documentation:

# module: data_load
kill_webkit_server()
    Kills all Xfvb and webkit servers that are no longer being used.

GetUsers(search_keyword)
    Uses about.me search feature to search for search_keyword and
    extracts all user_names. Will save user_names extracted while loading
    in event of connection failure. In event of failure, search_keyword is
    stored in to_scrape/incomplete.txt. Successfully extracted usernames
    are stored in user_list by keyword and log.txt stores search_keywords.
    
ScrapeUserData(user)
    Scrapes data from user username from about.me site. Returns a dict object
    with scraped data.
    
# module: aboutmeScraper

ScrapeSession()
    Creates scrape session, taking users from the lists provided in the SCRAPE_LIST
    tuple. Uses ScrapeUserData in data_load module to get data, stores data in pickle file
    in the user_data folder. Clears memory after every CLEAR_MEMORY scrapes.
    
# module: sql_insert
    Creates all tables where necessary. If tables already created, starts populating data
    that can be found in the user_data directory.
    
# module: settings
    Set speed, clear memory, search lists, and storage spaces, including the MySQL db settings.
    See settings.py for more information.

# module gen_query

    makequery.set_query(user=None, firstname=True, lastname=True,
          	phone=True, email=True, websites=True, 
          	company=True, jobs=True, linkedin=True,
          	twitter=True, fb=True, gplus=True,
          	pinterest=True, youtube=True, instagram=True,
          	wordpress=None, tumblr=None, blogger=None,
          	quora=None, vimeo=None, vine=None,
          	flickr=None, fitbit=None, px500=None,
          	dribbble=None, medium=None, behance=None,
          	github=None, etsy=None, foursquare=None,
          	kickstarter=None, soundcloud=None, yelp=None,
          	vk=None, strava=None, spotify=None,
          	wikipedia=None, goodreads=None, location=True,
          	weibo=None, interests=True, get_all=False, default=True)
          	
    	Sets the query parameters. Set True to make it search for all of 
    	the specific column. Insert a list or tuple of filters, and it will
    	be both True and will search for filters. Filters will default 'OR'
    	in the SQL query. Set get_all to True if all results desired. get_all
    	will work on postgres but not mysql.
    
    makequery.set_req(	user=None, firstname=None, lastname=None,
          	phone=None, email=None, websites=None, 
          	company=None, jobs=None, linkedin=None,
          	twitter=None, fb=None, gplus=None,
          	pinterest=None, youtube=None, instagram=None,
          	wordpress=None, tumblr=None, blogger=None,
	          quora=None, vimeo=None, vine=None,
        	  flickr=None, fitbit=None, px500=None,
          	dribbble=None, medium=None, behance=None,
          	github=None, etsy=None, foursquare=None,
          	kickstarter=None, soundcloud=None, yelp=None,
          	vk=None, strava=None, spotify=None,
          	wikipedia=None, goodreads=None, location=True,
          	weibo=None, interests=True, get_all=False)
          	
    	Make certain columns required to be found in query. Set True
    	to specific columns to change from LEFT JOIN to INNER JOIN in
    	query.
    
    makequery.gen_query()
    	Update query string after applying settings. You must call
    	this after making settings or the query string will not be updated.
    
    makequery.clear_all()
	Resets everything to default values.
    	Default columns is listed under:
    	self.columns = ['user', 'firstname', 'lastname', 'email', 'phone', 'jobs', 'company',
			'websites', 'linkedin', 'twitter', 'fb', 'gplus', 'pinterest', 'youtube',
			'instagram', 'location', 'interests']
						
    output_query(csv_or_json, output_file_name)
    	Generates csv or json file, with output_file_name as the name.
    	No need to put '.csv' or '.json' in output_file_name.
    	WARNING: This method is not part of the GeneralQuery class, so
    	there is no need to call it using makequery. Just a simple
    	output_query(params) is required.
    
