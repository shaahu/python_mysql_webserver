# this file redirects the api request and returns response
from flask import Flask, g

from api._req_notifications_ import query_notiication_list, store_notification
from api._req_story import query_all_stories
from api._req_user_ import user, store_user, update_token, user_login
from flaskr.db import get_db

app = Flask(__name__)


@app.before_request
def before_request():
    g.db = get_db()


# Notification request
# API get request for all notifications

@app.route('/story/all')
def get_all_stories():
    return query_all_stories()

@app.route('/api/notifications')
def get_notifications():
    return query_notiication_list()


# post request to store and get notifications
@app.route('/api/notifications', methods=['POST'])
def notification_create():
    return store_notification()


# get request to get user details
@app.route('/api/users')
def user_detail():
    return user()


# get request to store user details and fcm token
@app.route('/api/register', methods=['POST'])
def user_create():
    return store_user()


@app.route('/api/login', methods=['POST'])
def user_login_query():
    return user_login()
