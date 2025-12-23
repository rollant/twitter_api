import flask
from x_client import XClient

API_SECRET_FILE = "api_key.json"
DEFAULT_RESULTS_LIMIT = 30


app = flask.Flask(__name__)


@app.route("/hashtags/<hashtag>")
def get_hashtag(hashtag):
    limit = flask.request.args.get("limit", DEFAULT_RESULTS_LIMIT)
    return app.api_client.get_hashtag_posts(hashtag, max_results=limit)


@app.route("/users/<user>")
def get_user(user):
    limit = flask.request.args.get("limit", DEFAULT_RESULTS_LIMIT)
    return app.api_client.get_user_posts(user, max_results=limit)


if __name__ == '__main__':
    app.api_client = XClient()
    app.api_client.load_api_secret_from_file(API_SECRET_FILE)
    app.run('localhost', 8080, debug=True)
