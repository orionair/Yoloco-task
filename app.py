from flask import Flask
from connector import get_result

app = Flask(__name__)


@app.route('/<username>', methods=['POST', 'GET'])
def get_instagram_data(username):
    res = get_result(username)
    return res['data'], res['status_code']


if __name__ == '__main__':
    app.run()
