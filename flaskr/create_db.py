#!/usr/bin/python

import os
import sqlite3

from flaskr.db import DATABASE_DIR, DATABASE_PATH

if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)

conn = sqlite3.connect(DATABASE_PATH)

print("Opened database successfully")

conn.execute('DROP TABLE IF EXISTS user;')
conn.execute('DROP TABLE IF EXISTS notifications;')
conn.execute('DROP TABLE IF EXISTS story;')

conn.execute('''CREATE TABLE notifications
         (id INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
         notification_id            INT     NOT NULL,
         name           TEXT    NOT NULL,
         priority           TEXT    NOT NULL,
         count           INT    NOT NULL);''')

conn.execute('''CREATE TABLE user
         (id INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
         name           TEXT    NOT NULL,
         email          TEXT UNIQUE   NOT NULL,
         username       TEXT UNIQUE   NOT NULL,
         password       TEXT    NOT NULL,
         phone          INT  UNIQUE NOT NULL,
         fcm           TEXT,
         otp            INT);''')

story_query = '''CREATE TABLE story
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        story_art TEXT NOT NULL,
        story_title TEXT NOT NULL,
        story_body TEXT NOT NULL,
        elapsed DATETIME NOT NULL,
        author TEXT NOT NULL,
        category TEXT NOT NULL,
        likes INTEGER,
        dislikes INTEGER,
        comments INTEGER);'''
conn.execute(story_query)

conn.close()
print("Closed database successfully")
