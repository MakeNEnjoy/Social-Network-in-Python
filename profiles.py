from views import VIEWS
from auth import render_posts_from_user, get_username, get_id, make_post, follow, get_following, get_followers, unfollow, is_following

class profile_pages:
	def __init__(self):
		self.post = None

	def do_GET(self, path, user_id=None):

		sub_path = path[0]

		files = [
			VIEWS['begin'],
			VIEWS['navbar']['begin'],
			VIEWS['navbar']['normal']['home'],
			VIEWS['navbar']['normal']['login'],
			VIEWS['navbar']['normal']['register']]

		if(user_id is not None):
			files.append(VIEWS['navbar']['normal']['logout'])
			id_username = get_id(sub_path)
			try:
				if(path[1] == 'follow'):
					if(id_username != user_id and not is_following(user_id, id_username)):
						follow(user_id, id_username)
						files.append(VIEWS['redirect-to-main'])
					else:
						files.append(VIEWS['redirect-to-main'])
				elif(path[1] == 'unfollow'):
					if(id_username != user_id):
						unfollow(user_id, id_username)
						files.append(VIEWS['redirect-to-main'])
			except:
				pass

		user_data = [sub_path, 'Cool and witty one-liner',
                    len(get_following(get_id(sub_path))), len(get_followers(get_id(sub_path)))]

		files.extend([
			VIEWS['navbar']['end'],
			VIEWS['profile']['1'],
			[user_data[0]],
			VIEWS['profile']['2'],
			[user_data[1]],
			VIEWS['profile']['3'],
			[sub_path]])
		
		if(is_following(user_id, id_username)):
			files.append(VIEWS['profile']['3-5-unfollow'])
		else:
			files.append(VIEWS['profile']['3-5'])

		files.extend([
			[user_data[2]],
			VIEWS['profile']['4'],
			[user_data[3]],
			VIEWS['profile']['5'],
		])
		if(get_username(user_id) == sub_path):
			files.append(VIEWS['profile']['comment-box'])
			if(self.post is not None):
				make_post(user_id, self.post)
		
		files.extend(render_posts_from_user(get_id(sub_path)))
		self.post = None
		return files

	def do_POST(self, post_data):
		self.post = post_data['message'.encode('utf-8')][0].decode("utf-8")
