from auth import login_account
from views import VIEWS


class login:
	def __init__(self):
		self.response = None

	def do_GET(self, user_id=None):
		files = [
			VIEWS['begin'],
			VIEWS['navbar']['begin'],
			VIEWS['navbar']['normal']['home'],
			VIEWS['navbar']['active']['login'],
			VIEWS['navbar']['normal']['register']]
		if(user_id is not None):
			files.append(VIEWS['navbar']['normal']['logout'])
		files.extend([
			VIEWS['navbar']['end'],
			VIEWS['login-start']])
		if(self.response == "Username and password don't match"):
			files.append(VIEWS['messages']['username-and-password-dont-match'])
		files.extend([
			VIEWS['login-end'],
            VIEWS['end']])
		if(self.response == "Login successful"):
			files.append(VIEWS['redirect-to-main'])

		self.response = None
		return files

	def do_POST(self, post_data):
		self.response, user_id = login_account(post_data['username'.encode('utf-8')][0].decode("utf-8"),
                                   post_data['password'.encode('utf-8')][0].decode("utf-8"))
		return user_id
