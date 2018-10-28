import gspread
from oauth2client.service_account import ServiceAccountCredentials

import uuid

from views import VIEWS

import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Authentication').sheet1

cookies = client.open('Authentication').get_worksheet(1)

user_posts = client.open('Authentication').get_worksheet(2)

followers = client.open('Authentication').get_worksheet(3)

def register_account(username, password, confirm_password):
	if(not password == confirm_password):
		return "Passwords don't match"
	for user in sheet.col_values(2):
		if(user == username):
			return "Username already exists"
	user_id = int(sheet.col_values(1)[-1]) + 1
	sheet.append_row([user_id, str(username), str(password)])
	follow(user_id, 0)
	return "Account registered"
	
def login_account(username, password):
	for user in sheet.get_all_records():
		if(str(user['username']) == username and str(user['password']) == password):
			session = create_session(username)
			return "Login successful", session
	return "Username and password don't match", None

def get_username(user_id):
	for user in sheet.get_all_records():
		if(user_id == user['id']):
			return user['username']

def get_id(username):
	for user in sheet.get_all_records():
		if(username == user['username']):
			return user['id']


def create_session(username):
	for user in sheet.get_all_records():
		if(user['username'] == username):
			user_id = uuid.uuid4().hex
			cookies.append_row([int(user['id']), user_id, 0])
			return user_id

def check_session(cookie):
	for user in cookies.get_all_records():
		if(user['cookie'] == cookie and user['expired'] == 0):
			return True, user['id']
	return False, None

def make_post(user_id, message):
	user_posts.append_row(
		[user_id, int(user_posts.col_values(2)[-1]) + 1, message])


def render_posts_from_user(user_id):
	posts = []
	for post in user_posts.get_all_records():
		if(post['user_id'] == user_id):
			posts.append((get_username(post['user_id']), post['post']))
	posts.reverse()
	files = [VIEWS['main-start']]
	for post in posts:
		files.append(VIEWS['post-start'])
		files.append([post[0]])
		files.append(VIEWS['post-middle'])
		files.append([post[1]])
		files.append(VIEWS['post-end'])
	files.append(VIEWS['main-end'])
	return files


def follow(user_id, follow_id):
	followers.append_row([user_id, follow_id])

def is_following(user_id, follow_id):
	for row in followers.get_all_records():
		if(row['user_id'] == user_id and row['following_id'] == follow_id):
			return True
	return False

def get_following(user_id):
	following = []
	for row in followers.get_all_records():
		if(row['user_id'] == user_id):
			following.append(row['following_id'])
	return following

def get_followers(user_id):
	following_users = []
	for row in followers.get_all_records():
		if(row['following_id'] == user_id):
			following_users.append(row['user_id'])
	return following_users


def unfollow(user_id, follow_id):
	i = 2
	for row in followers.get_all_records():
		if(row['user_id'] == user_id and row['following_id'] == follow_id):
			followers.delete_row(i)
		i += 1
			


def render_posts_for_home(user_id):
	#posts = [('Root', 'Welcome to bookface'), ('Root', 'Second example post!')]
	posts = []
	for row in followers.get_all_records():
		if(row['user_id'] == user_id):
			posts_from_user = []
			for post in user_posts.get_all_records():
				if(post['user_id'] == row['following_id']):
					posts_from_user.append((get_username(post['user_id']), post['post']))
			posts.extend(posts_from_user)

	posts.reverse()
	files = [VIEWS['main-start']]
	for post in posts:
		files.append(VIEWS['post-start'])
		files.append([post[0]])
		files.append(VIEWS['post-middle'])
		files.append([post[1]])
		files.append(VIEWS['post-end'])
	files.append(VIEWS['main-end'])
	return files
