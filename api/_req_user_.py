import sqlite3

from flask import request, g

from utils.uitils import JSON_MIME_TYPE, onsuccess_response, onerror_response, is_data_not_exist, is_data_exist

import json


# fetch all user details
def user():
    try:
        cursor = g.db.execute('SELECT id, name, fcm_token FROM user;')
    except:
        if request.content_type != JSON_MIME_TYPE:
            return onerror_response('No data available')

    user = [{
        'id': row[0],
        'name': row[1],
        'fcm_token': row[2]
    } for row in cursor.fetchall()]

    return onsuccess_response(user)


# store new user
def store_user():
    print(request)
    print(request.content_type)
    # if request.content_type != JSON_MIME_TYPE:
    #     return onerror_response('Invalid Content Type')

    data = request.json
    if not all([data.get('name')]):
        return onerror_response('Missing field/s (name) (fcm_token)')

    params = {
        'name': data['name'],
        'email': data['email'],
        'username': data['username'],
        'password': data['password'],
        'phone': data['phone'],
        'fcm': data['fcm']
    }

    query = 'INSERT INTO user ("name", "email","username", "password", "phone",  "fcm") ' \
            'VALUES (:name,  :email, :username, :password, :phone, :fcm);'

    try:
        g.db.execute(query, params)
    except sqlite3.IntegrityError as s:
        stringer = str(s)
        data = [{'exception': stringer}]
        return onerror_response(data)
        pass

    g.db.commit()

    return user_details_resp()



# returns user details
def user_details_resp():
    try:
        cursor = g.db.execute('SELECT * FROM user ORDER BY id DESC LIMIT 1;')
    except:
        if request.content_type != JSON_MIME_TYPE:
            return onerror_response('No data available')

    user = [{
        'id': row[0],
        'name': row[1],
        'fcm_token': row[2]
    } for row in cursor.fetchall()]

    data = [{'registration': "ok"}]

    return onsuccess_response(data)


# update fcm token
def update_token(user_id):
    # if request.content_type != JSON_MIME_TYPE:
    #     return onerror_response('Invalid Content Type')

    data = request.json
    if not all([data.get('fcm_token')]):
        return onerror_response('Missing field/s (fcm_token)')

    params = {'id': user_id}
    query = 'SELECT * FROM user WHERE user.id = :id'

    cursor = g.db.execute(query, params)
    if is_data_not_exist(cursor):
        return onerror_response("No User exist")

    # Update it
    token = data.get('fcm_token')
    g.db.execute('''UPDATE user SET fcm_token = ? WHERE id = ?''', (token, user_id))
    g.db.commit()

    params = {'id': user_id}
    query = 'SELECT * FROM user WHERE user.id = :id'
    cursor = g.db.execute(query, params)

    user = [{
        'id': row[0],
        'name': row[1],
        'fcm_token': row[2]
    } for row in cursor.fetchall()]

    return onsuccess_response(user)


# returns registered user to collect fcm token
def get_users():
    try:
        cursor = g.db.execute('SELECT fcm_token FROM user;')
    except:
        if request.content_type != JSON_MIME_TYPE:
            return onerror_response('No data available')

    user = [{
        'fcm_token': row[0]
    } for row in cursor.fetchall()]

    fcm_reg_list = []
    for chunks in user:
        for attribute, value in chunks.items():
            fcm_reg_list.append('device ' + value)
    return fcm_reg_list


def user_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    params = {'uname': username, 'pword': password}
    query = 'SELECT * FROM user where username = :uname AND password = :pword'
    try:
        cursor = g.db.execute(query, params)
    except sqlite3.IntegrityError as s:
        print(s)


    user = [{
        'name': row[1],
        'email': row[2],
        'username': row[3],
        'password': row[4],
        'phone': row[5]
    } for row in cursor.fetchall()]

    print(user)

    if is_data_exist(user):
        return onsuccess_response(user)
    else:
        failed = [{'login': 'auth_failed'}]
        return onerror_response(failed)
