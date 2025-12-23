## Prerequisites
You will need [X developer account](https://developer.x.com/en/portal/petition/essential/basic-info). Once set up, API Bearer token can be generated under Projects and Apps -> {project name} -> {app name} -> Keys and tokens. Once set up, Bearer token must be placed in `api_key.json` file. Example file can be found under `api_key.json.in`

IMPORTANT: Do not publish Bearer token on Github or other public spaces.

## Local setup
  1. Create virtualenv
```
$ virtualenv -p "`which python3.11`" .venv 
```
This will ensure this application is run on correct version of Python. This step needs to be done only once 

  2. Activate virtualenv
```
$ . .venv/bin/activate
```
This step will be needed every time you run the application in the new shell.

  3. Install required packages
```
pip3 install -r requirements.txt
```
This step is needed to be done only once

  4. Run the application
```
$ python3 main.py
```

# Usage
Example usage:
```
$ curl 'http://localhost:8080/users/XDevelopers?limit=10'
```

That will return 10 latest posts from the user XDevelopers.
There are two endpoints available: `/users/` and `/hashtags/`, returning latest posts from given user or given hashtag respectively.


Parameters (for both endpoints):
  * Target user or hashtag specified in the path (i. e. `/users/XDevelopers` or `/hashtags/grumpycat`). Only one can be specified (i. e. querying tweets from two users in one reqiest is impossible)
  * `limit`: Limit the number of latest posts that can be retrieved. Please note that at the time of this writing it must be between 10 and 100 (at least for free accounts).

Internally, both endpoints call X search API, [/tweets/search/](https://docs.x.com/x-api/posts/search/). Due to limitations of the free tier, only `/tweets/search/recent` has been tested.
