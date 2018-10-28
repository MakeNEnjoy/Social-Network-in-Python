from auth import register_account, render_posts_for_home
from views import VIEWS

class homePage:
	def do_GET(self, user_id = None):

		files = [
			VIEWS['begin'],
			VIEWS['navbar']['begin'],
			VIEWS['navbar']['active']['home'],
			VIEWS['navbar']['normal']['login'],
			VIEWS['navbar']['normal']['register']]
		if(user_id is not None):
			files.append(VIEWS['navbar']['normal']['logout'])
		files.extend([
			VIEWS['navbar']['end']])
		if(user_id is not None):
			files.extend(render_posts_for_home(user_id))
				
		else:
			files.append(VIEWS['landing-page'])
		files.append(VIEWS['end'])
		return files
	def do_POST(self, post_data):
		return
