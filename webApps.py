from home import homePage
from register import register
from thanks import thanks
from login import login
from profiles import profile_pages

#	Path: App Class
apps = {
	'/': homePage(),
	'/register': register(),
	'/thanks': thanks(),
	'/login': login()
}

nested_webapps = {
	'u': profile_pages(),
}