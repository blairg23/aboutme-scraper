import settings

#WARNING: This will reset all logs. 
#The already scraped files will still be retained in the user_data folder.
#You will have to manually delete those files.

open('%s%s' % (settings.USER_LIST_DIR, settings.USER_LIST_LOG), 'w').close()
open('%s%s' % (settings.COMPLETED_PATH, settings.COMPLETED_SEARCH_TERMS), 'w').close()
open('%s%s' % (settings.COMPLETED_PATH, settings.COMPLETED_USER_LIST), 'w').close()
open('%s%s' % (settings.USER_LIST_DIR, settings.USER_DATA_POPULATED), 'w').close()
