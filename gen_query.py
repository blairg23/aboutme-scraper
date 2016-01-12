import MySQLdb
import settings
import pandas as pd
import json

class GeneralQuery:
    def __init__(self):
        self.query_keys = {
            'user': {'n_short': 'u', 'qry': True},
			'firstname': {'n_short': 'fna', 'ux_short': 'ufna', 'qry': False, 'filters': [], 'req': False},
			'lastname': {'n_short': 'lna', 'ux_short': 'ulna', 'qry': False, 'filters': [], 'req': False},
			'email': {'n_short': 'em', 'ux_short': 'uem', 'qry': False, 'filters': [], 'req': False},
			'phone': {'n_short': 'ph', 'ux_short': 'uph', 'qry': False, 'filters': [], 'req': False},
			'jobs': {'n_short': 'jo', 'ux_short': 'ujo', 'qry': False, 'filters': [], 'req': False},
			'company': {'n_short': 'cmp', 'ux_short': 'ucmp', 'qry': False, 'filters': [], 'req': False},
			'websites': {'n_short': 'web', 'ux_short': 'uweb', 'qry': False, 'filters': [], 'req': False},
			'linkedin': {'n_short': 'lki', 'ux_short': 'ulki', 'qry': False, 'filters': [], 'req': False},
			'twitter': {'n_short': 'twit', 'ux_short': 'utwit', 'qry': False, 'filters': [], 'req': False},
			'fb': {'n_short': 'facb', 'ux_short': 'ufacb', 'qry': False, 'filters': [], 'req': False},
			'gplus': {'n_short': 'goop', 'ux_short': 'ugoop', 'qry': False, 'filters': [], 'req': False},
			'pinterest': {'n_short': 'pint', 'ux_short': 'upint', 'qry': False, 'filters': [], 'req': False},
			'youtube': {'n_short': 'yut', 'ux_short': 'uyut', 'qry': False, 'filters': [], 'req': False},
			'instagram': {'n_short': 'ing', 'ux_short': 'uing', 'qry': False, 'filters': [], 'req': False},
			'wordpress': {'n_short': 'wrdp', 'ux_short': 'uwrdp', 'qry': False, 'filters': [], 'req': False},
			'tumblr': {'n_short': 'tmbl', 'ux_short': 'utmbl', 'qry': False, 'filters': [], 'req': False},
			'blogger': {'n_short': 'blogr', 'ux_short': 'ublogr', 'qry': False, 'filters': [], 'req': False},
			'quora': {'n_short': 'qra', 'ux_short': 'uqra', 'qry': False, 'filters': [], 'req': False},
			'vimeo': {'n_short': 'vmo', 'ux_short': 'uvmo', 'qry': False, 'filters': [], 'req': False},
			'vine': {'n_short': 'vne', 'ux_short': 'uvne', 'qry': False, 'filters': [], 'req': False},
			'flickr': {'n_short': 'flir', 'ux_short': 'uflir', 'qry': False, 'filters': [], 'req': False},
			'fitbit': {'n_short': 'fitb', 'ux_short': 'ufitb', 'qry': False, 'filters': [], 'req': False},
			'500px': {'n_short': 'fipx', 'ux_short': 'ufipx', 'qry': False, 'filters': [], 'req': False},
			'dribbble': {'n_short': 'drbl', 'ux_short': 'udrbl', 'qry': False, 'filters': [], 'req': False},
			'medium': {'n_short': 'mdum', 'ux_short': 'umdum', 'qry': False, 'filters': [], 'req': False},
			'behance': {'n_short': 'bhce', 'ux_short': 'ubhce', 'qry': False, 'filters': [], 'req': False},
			'github': {'n_short': 'ghub', 'ux_short': 'ughub', 'qry': False, 'filters': [], 'req': False},
			'etsy': {'n_short': 'etsc', 'ux_short': 'uetsc', 'qry': False, 'filters': [], 'req': False},
			'foursquare': {'n_short': 'frsq', 'ux_short': 'ufrsq', 'qry': False, 'filters': [], 'req': False},
			'kickstarter': {'n_short': 'kiks', 'ux_short': 'ukiks', 'qry': False, 'filters': [], 'req': False},
			'soundcloud': {'n_short': 'scld', 'ux_short': 'uscld', 'qry': False, 'filters': [], 'req': False},
			'yelp': {'n_short': 'yeal', 'ux_short': 'uyeal', 'qry': False, 'filters': [], 'req': False},
			'vk': {'n_short': 'vka', 'ux_short': 'uvka', 'qry': False, 'filters': [], 'req': False},
			'strava': {'n_short': 'stva', 'ux_short': 'ustva', 'qry': False, 'filters': [], 'req': False},
			'spotify': {'n_short': 'sptfy', 'ux_short': 'usptfy', 'qry': False, 'filters': [], 'req': False},
			'wikipedia': {'n_short': 'wiki', 'ux_short': 'uwiki', 'qry': False, 'filters': [], 'req': False},
			'goodreads': {'n_short': 'gdre', 'ux_short': 'ugdre', 'qry': False, 'filters': [], 'req': False},
			'location': {'n_short': 'loc', 'ux_short': 'uloc', 'qry': False, 'filters': [], 'req': False},
			'weibo': {'n_short': 'wei', 'ux_short': 'uwei', 'qry': False, 'filters': [], 'req': False},
			'interests': {'n_short': 'intr', 'ux_short': 'uintr', 'qry': False, 'filters': [], 'req': False},
		}
    
        self.query_string = None
        self.columns = ['user', 'firstname', 'lastname', 'email', 'phone', 'jobs', 'company',
						'websites', 'linkedin', 'twitter', 'fb', 'gplus', 'pinterest', 'youtube',
						'instagram', 'location', 'interests']

    def clear_all(self):
        for key, value in self.query_keys.iteritems():
            self.query_keys[key]['qry'] = False
            self.query_keys[key]['req'] = False
            self.query_keys[key]['filters'] = []

    def gen_gq_select(self):
        select_str = "SELECT DISTINCT u.user_name as username, "
        for unit in self.columns:
            if unit == 'user':
                pass
            elif self.query_keys[unit]['qry'] == True:
                col_ptype = "max({0}.{1}_name) as {1}, ".format(self.query_keys[unit]['n_short'], unit)
                select_str += col_ptype
        select_str = select_str[:-2]
        select_str += ' FROM user u '
        return select_str

    def gen_gq_n_ux(self):
        n_ux_str = ''
        for unit in self.columns:
            if unit == 'user':
                pass
            elif self.query_keys[unit]['qry'] == False:
                pass
            else:
                req_or = "INNER JOIN" if self.query_keys[unit]['req'] else "LEFT JOIN"
                qux_str = "{0} user_{1} {2} ON (u.user_id = {2}.user_id) ".format(req_or, unit, self.query_keys[unit]['ux_short'])
                qn_str = "{0} {1} {2} ON ({2}.{1}_id = {3}.{1}_id) ".format(req_or, unit, self.query_keys[unit]['n_short'], self.query_keys[unit]['ux_short'])
                main_str = qux_str + qn_str
                n_ux_str += main_str
        return n_ux_str

    def apply_filters(self):
        init_fil_str = "WHERE "
        for unit in self.columns:
            if unit == 'user':
                pass
            elif len(self.query_keys[unit]['filters']) == 0:
                pass
            else:
                for filt in self.query_keys[unit]['filters']:
                    fil_str = '({0}.{1}_name = "{2}") OR '.format(self.query_keys[unit]['n_short'], unit, filt)
                    init_fil_str += fil_str
        init_fil_str = init_fil_str[:-4]
        if len(init_fil_str) < 10:
            return ''
        else:
            return init_fil_str

    def gen_query(self):
        gen_str = ""
        gen_str += self.gen_gq_select()
        gen_str += self.gen_gq_n_ux()
        gen_str += self.apply_filters()
        gen_str += ' GROUP BY u.user_name'
        gen_str += ';'
        self.query_string = gen_str

    def set_req(
            self,
            user=None, firstname=None, lastname=None,
            email=None, phone=None, jobs=None,
            company=None, websites=None, linkedin=None,
            twitter=None, fb=None, gplus=None,
            pinterest=None, youtube=None, instagram=None,
            wordpress=None, tumblr=None, blogger=None,
            quora=None, vimeo=None, vine=None,
            flickr=None, fitbit=None, px500=None,
            dribbble=None, medium=None, behance=None,
            github=None, etsy=None, foursquare=None,
            kickstarter=None, soundcloud=None, yelp=None,
            vk=None, strava=None, spotify=None,
            wikipedia=None, goodreads=None, location=None,
            weibo=None, interests=None, get_all=False):
            """Set required flag for specific queries."""
            if get_all == True:
                for key, value in self.query_keys.iteritems():
                    self.query_keys[key]['req'] = True
                return True
            sq_args = locals()
            for key, value in sq_args.iteritems():
                if key == 'self':
                    pass
                elif sq_args[key] == True:
                    self.query_keys[key]['req'] = True

    def set_query(
            self,
            user=None, firstname=True, lastname=True,
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
            weibo=None, interests=True, get_all=False, default=True):
        """Enter True for all, else [a, b, c] for specific."""
        if get_all == True:
            for key, value in self.query_keys.iteritems():
                self.query_keys[key]['qry'] = True
            return True
        sq_args = locals()
        for key, value in sq_args.iteritems():
            if key == 'self':
                pass
            elif key == 'default':
				pass
            elif sq_args[key] == None:
                pass
            elif isinstance(sq_args[key], (bool)):
                if sq_args[key] == True:
                    self.query_keys[key]['qry'] = True
            elif isinstance(sq_args[key], (list, tuple)):
                self.query_keys[key]['qry'] = True
                for filt in sq_args[key]:
                    self.query_keys[key]['filters'].append(filt)
        if default == False:
             for key, value in sq_args.iteritems():
                 if key not in self.columns:
                     self.columns.append(key)

if len(settings.MYSQL_PORT) > 0:
	db = MySQLdb.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PWD, settings.MYSQL_DB_NAME, settings.MYSQL_PORT)
else:
	db = MySQLdb.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PWD, settings.MYSQL_DB_NAME)


makequery = GeneralQuery()
makequery.set_query()
makequery.gen_query()

def output_query(csv_or_json, output_name, query_string=makequery.query_string, datb=db):
	df_mysql = pd.read_sql(makequery.query_string, db)
	if csv_or_json == 'csv':
		df_mysql.to_csv('%s.csv' % output_name, index=False)
	elif csv_or_json == 'json':
		tmp_js = df_mysql.to_json()
		with open('%s.json' % output_name, 'w') as jf:
			json.dump(tmp_js, jf)
