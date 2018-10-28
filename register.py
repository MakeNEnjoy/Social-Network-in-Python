from auth import register_account
from views import VIEWS

class register:
	def __init__(self):
		self.response = None

	def do_GET(self, user_id=None):
		files = [
			VIEWS['begin'],
			VIEWS['navbar']['begin'],
			VIEWS['navbar']['normal']['home'],
			VIEWS['navbar']['normal']['login'],
			VIEWS['navbar']['active']['register']]
		if(user_id is not None):
			files.append(VIEWS['navbar']['normal']['logout'])
		files.extend([
			VIEWS['navbar']['end'],
			VIEWS['register-start']])
		if(self.response is not None):
			if(self.response == "Passwords don't match"):
				files.append(VIEWS['messages']['passwords-dont-match'])
			elif(self.response == "Username already exists"):
				files.append(VIEWS['messages']['username-already-exists'])
			elif(self.response == "Account registered"):
				files.append(VIEWS['redirect-to-thanks'])
		files.extend([ 
					VIEWS['register-end'],
                    VIEWS['end']
					])

		self.response = None
		return files


	def do_POST(self, post_data):
		self.response = register_account(post_data['username'.encode('utf-8')][0].decode("utf-8"),
                   post_data['password'.encode('utf-8')][0].decode("utf-8"),
                   post_data['confirm_password'.encode('utf-8')][0].decode("utf-8"))
