#!/usr/bin/python

import os
import sqlite3
import datetime as dt

from flaskr.db import DATABASE_DIR, DATABASE_PATH

if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)

conn = sqlite3.connect(DATABASE_PATH)
c = conn.cursor()
values = [DATABASE_DIR + "img.jpg", "abc", "once upon a time", dt.datetime.now().strftime("%d,%B %Y %H:%M"), "shahu"]
c.execute('''INSERT INTO story (story_art,story_title,story_body,elapsed,author) VALUES (?,?,?,?,?)''', values)


