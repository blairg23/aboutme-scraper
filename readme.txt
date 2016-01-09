module: data_load
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
    
module: aboutmeScraper

ScrapeSession()
    Creates scrape session, taking users from the lists provided in the SCRAPE_LIST
    tuple. Uses ScrapeUserData in data_load module to get data, stores data in pickle file
    in the user_data folder. Clears memory after every CLEAR_MEMORY scrapes.
    
module: sql_insert
    Creates all tables where necessary. If tables already created, starts populating data
    that can be found in the user_data directory.
    
module: settings
    Set speed, clear memory, search lists, and storage spaces, including the MySQL db settings.
    See settings.py for more information.
