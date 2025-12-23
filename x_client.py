import json
import requests

API_PROTO = 'https'
API_HOST = 'api.x.com'
API_VERSION = '2'


class XClient:
    base_url = f'{API_PROTO}://{API_HOST}/{API_VERSION}'

    def __init__(self):
        self._api_key = None

    # Other methods, such as env variables, may be considered in the future
    def load_api_secret_from_file(self, api_secret_file):
        """
        Reads API key from JSON file. See README.md for details
        Params:
        api_secret_file: path to a file with API secret.
        """
        with open(api_secret_file) as f:
            data = json.load(f)
        if 'x_api_key' in data:
            self._api_key = data['x_api_key']
        else:
            raise Exception(f'Cannot find x_api_key in {api_secret_file}')

    def _get_auth_header(self):
        return {'Authorization': f'Bearer {self._api_key}'}

    def get_user_posts(self, user, max_results=30):
        """
        Get most recent posts from the user
        Params:
        user: username of the target user
        max_results: limit the number of tweets returned
        """
        query = f'from:{user}'
        return self._make_search_query(query, max_results=max_results)

    def get_hashtag_posts(self, hashtag, max_results=30):
        """
        Get most recent posts for given hashtag
        Params:
        hashtag: target hashtag (without #)
        max_results: limit the number of tweets returned
        """
        query = f'#{hashtag}'
        return self._make_search_query(query, max_results=max_results)

    def _make_search_query(self, query=None, search_all=False, max_results=30):
        """
        Construct query for X search API. See
        https://docs.x.com/x-api/posts/search-recent-posts for usage details.
        Params:
        query: query text.
        search_all: search for all tweets instead of recent only
        max_results: limit the number of tweets returned
        """
        path = '/tweets/search/'
        # Note that only recent tweets are available on the free tier
        if search_all:
            path += 'all'
        else:
            path += 'recent'

        params = {}
        # Note that search with empty query is valid.
        # E. g.: /tweets/recent?max_results=10
        if query:
            params['query'] = query
        if max_results:
            params['max_results'] = max_results

        return self.make_request(path, **params)

    def make_request(self, path, **params):
        """
        Make a request to X API
        Params:
        path: URL path
        **params: GET parameters are added as keyword arguments
        Returns:
        On success:
        result["data"], status code
        On error:
        result, status code
        """
        url = self.base_url + path
        headers = self._get_auth_header()
        r = requests.get(url, params=params, headers=headers)
        result = r.json()
        if r.ok:
            # On successful request, post data is contained in "data" field.
            return result['data'], r.status_code
        else:
            # Here we get an error message and an explanation
            return result, r.status_code
