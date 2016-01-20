import settings

open('%s%s' % (settings.USER_LIST_DIR, settings.USER_LIST_LOG), 'w').close()
open('%s%s' % (settings.COMPLETED_PATH, settings.COMPLETED_SEARCH_TERMS), 'w').close()
open('%s%s' % (settings.COMPLETED_PATH, settings.COMPLETED_USER_LIST), 'w').close()
