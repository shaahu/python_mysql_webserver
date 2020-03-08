import json
from flask import request, g
from utils.uitils import json_response, JSON_MIME_TYPE, onerror_response, onsuccess_response


# returns all stories
def query_all_stories():
    try:
        cursor = g.db.execute(
            'SELECT id, story_art, story_title, story_body, elapsed, author, category, likes, dislikes, comments FROM story;')

    except Exception as e:
        print(e)
        if request.content_type != JSON_MIME_TYPE:
            return onerror_response('No data available')

    stories = [{
        'id': row[0],
        'story_art': row[1],
        'story_title': row[2],
        'story_body': row[3],
        'elapsed': row[4],
        'author': row[5],
        'category': row[6],
        'likes': row[7],
        'dislikes': row[8],
        'comments': row[9]
    } for row in cursor.fetchall()]

    return onsuccess_response(stories)
