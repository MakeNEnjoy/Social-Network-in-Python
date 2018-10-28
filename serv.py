#TODO: Limit charcter use in username creation Sunday 07/10/2018
#TODO: XSS attacks are possible Saturday 13/10/2018

from views import VIEWS

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from auth import check_session

from http.cookies import SimpleCookie

from socketserver import ThreadingMixIn
import threading

import os, os.path

from webApps import apps, nested_webapps

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)



class Serv(BaseHTTPRequestHandler):

	def do_GET(self, post_data=None):
		user_id = None
		self.id = None
		for header in self.headers._headers:
			if(header[0] == 'Cookie'):
				cookie = SimpleCookie()
				cookie.load(header[1])
				cookies = {}
				for key, morsel in cookie.items():
					cookies[key] = morsel.value
				if('sess' in cookies):
					self.logged_in, self.id = check_session(cookies['sess'])
		try:
			url = urlparse(self.path)
			found = False

			PARSED_URL = os.path.split(url.path)

			for app in apps:

				if(url.path == '/logout'):
					found = True
					web_page = [VIEWS['redirect-to-main']]
					self.send_response(200)
					self.send_header(
						'Set-Cookie', 'sess=deleted; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT')
				
				if(url.path == app):
					found = True
					web_app = apps[app]

					if(post_data is not None):
						user_id = web_app.do_POST(post_data)
							

					web_page = web_app.do_GET(user_id = self.id)
					self.send_response(200)
					break

			
			if(not found):

				PARSED_URL = url.path.split('/')[1:]

				for app in nested_webapps:
					if(PARSED_URL[0] == app):

						found = True

						web_app = nested_webapps[app]

						if(post_data is not None):
							user_id = web_app.do_POST(post_data)

						web_page = web_app.do_GET(PARSED_URL[1:], user_id=self.id)
						self.send_response(200)
						break

					

			if(not found):
				web_page = "App not found"
				self.send_response(404)
				return
		except:
			web_page = "File not found"
			self.send_response(404)
		if(user_id is not None):
			print('Cookie Sent')
			self.send_header('Set-Cookie', 'sess=' + user_id)
		self.end_headers()
		for part in web_page:
			if(isinstance(part, (list,))):
				self.wfile.write(bytes(str(part[0]), 'utf-8'))
			else:
				self.wfile.write(bytes(open(part).read(), 'utf-8'))

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		body = self.rfile.read(content_length)
		fields = parse_qs(body)

		self.do_GET(post_data=fields)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ This class allows to handle requests in separated threads.
        No further content needed, don't touch this. """


#httpd = HTTPServer(('localhost', 8080), Serv)
httpd = ThreadedHTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()
