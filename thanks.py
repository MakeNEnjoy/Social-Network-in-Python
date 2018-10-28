from views import VIEWS


class thanks:
	def do_GET(self, user_id=None):

		files = [
			VIEWS['begin'],
			VIEWS['navbar']['begin'],
			VIEWS['navbar']['normal']['home'],
			VIEWS['navbar']['normal']['login'],
			VIEWS['navbar']['normal']['register']]
		if(user_id is not None):
			files.append(VIEWS['navbar']['normal']['logout'])
		files.extend([
			VIEWS['navbar']['end'],
			VIEWS['post-sign-up-start'],
			VIEWS['messages']['account-registered'],
			VIEWS['post-sign-up-end'],
			VIEWS['end']])
		return files

	def do_POST(self, post_data):
		return
