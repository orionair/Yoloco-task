import requests
import json


def get_result(user):

    end_point = f'https://www.instagram.com/{user}/?__a=1'

    response = requests.get(end_point)

    if response.status_code == 404:
        result = {'data': {'error': 'User not found'},
                  'status_code': 404}
        return result
    elif response.status_code != 200:
        result = {'data': {'error': 'Unknown problem'},
                  'status_code': response.status_code}
        return result
    else:
        try:
            user_data = json.loads(response.content.decode())['graphql']['user']

            user_id = int(user_data['id'])

            user_name = user_data['username']

            subscribers = int(user_data['edge_followed_by']['count'])

            posts = user_data['edge_owner_to_timeline_media']['edges']

            comments_count = 0
            likes_count = 0

            for post in posts:
                comments_count += int(post['node']['edge_media_to_comment']['count'])
                likes_count = int(post['node']['edge_liked_by']['count'])

            avg_comments = comments_count / len(posts)
            avg_likes = likes_count / len(posts)

            er = (avg_likes + avg_comments) / subscribers

            result = {'data': {'User_ID': user_id, 'ER': er, 'Username': user_name},
                      'status_code': 200}

            return result
        except KeyError:
            result = {'data': {'error': 'Cannot parse instagram response'},
                      'status_code': 500}
            return result
