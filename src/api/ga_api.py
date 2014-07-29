#!/usr/bin/python
import sys
from sys import maxint
import time
import twitter
from functools import partial
from urllib2 import URLError
import os.path
import json


class BigTwitterBrother():
    """
    class twitter api functions
    """

    def __init__(self, twitter_id=None, twitter_name=None):
        self.id = twitter_id
        self.name = twitter_name

    @staticmethod
    def get_api():
        if os.path.exists('credentials'):
            dump = open('credentials', 'rb').read()
            creds = json.loads(dump)
        else:
            print "No credentials: create file with credentials"
            exit(0)

        consumer_key = creds['consumer_key']
        consumer_secret = creds['consumer_secret']
        oauth_token = creds['oauth_token']
        oauth_token_secret = creds['oauth_token_secret']

        if "" in [consumer_key, consumer_secret, oauth_token, oauth_token_secret]:
            print "No credentials: input data with credentials"
            exit(0)

        auth = twitter.oauth.OAuth(oauth_token, oauth_token_secret, consumer_key, consumer_secret)

        twitter_api = twitter.Twitter(auth=auth)
        return twitter_api

    def get_profile(self, twitter_api):
        assert (not self.name) != (not self.id), "Must have screen_names or user_ids, but not both"
        items_to_info = {}
        items = self.name or self.id

        while len(items) > 0:
            items_str = ','.join([str(item) for item in items[:100]])
            items = items[100:]

        if self.name:
            response = self.make_request(twitter_api.users.lookup, screen_name=items_str)
        else:
            response = self.make_request(twitter_api.users.lookup, user_id=items_str)

        for user_info in response:
            if self.name:
                items_to_info[user_info['screen_name']] = user_info
            else:
                items_to_info[user_info['id']] = user_info
            return items_to_info

    @staticmethod
    def make_request(twitter_api_func, max_errors=10, *args, **kw):

        def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):

            if wait_period > 3600:
                print >> sys.stderr, 'Too many retries. Quitting.'
                raise e
            if e.e.code == 401:
                print >> sys.stderr, 'Encountered 401 Error (Not Authorized)'
                return None
            elif e.e.code == 404:
                print >> sys.stderr, 'Encountered 404 Error (Not Found)'
                return None
            elif e.e.code == 429:
                print >> sys.stderr, 'Encountered 429 Error (Rate Limit Exceeded)'
                if sleep_when_rate_limited:
                    print >> sys.stderr, "Retrying in 15 minutes...ZZZ..."
                    sys.stderr.flush()
                    time.sleep(60 * 15 + 5)
                    print sys.stderr, '...ZZZ...Awake now and trying again.'
                    return 2
                else:
                    raise e
            elif e.e.code in (500, 502, 503, 504):
                print >> sys.stderr, 'Encountered %i Error . Retrying in %i seconds' % (e.e.code, wait_period)
                time.sleep(wait_period)
                wait_period *= 1.5
                return wait_period
            else:
                raise e

        wait_period = 2
        error_count = 0

        while True:
            try:
                return twitter_api_func(*args, **kw)
            except twitter.api.TwitterHTTPError, e:
                error_count = 0
                wait_period = handle_twitter_http_error(e, wait_period)
                if wait_period is None:
                    return
            except URLError, e:
                error_count += 1
                print >> sys.stderr, "URLError encountered. Continuing."
            if error_count > max_errors:
                print >> sys.stderr, "Too many consecutive errors...bailing out."
                raise

    def get_ffi(self, twitter_api, screen_name=None, user_id=None, friends_limit=maxint, followers_limit=maxint):

        assert (screen_name != None) != (user_id != None), "Must have screen_name or user_id but not both"

        get_friends_ids = partial(self.make_request, twitter_api.friends.ids, count=5000)
        get_followers_ids = partial(self.make_request, twitter_api.followers.ids, count=5000)
        friends_ids, followers_ids = [], []

        for twitter_api_func, limit, ids, label in [[get_friends_ids, friends_limit, friends_ids, "friends"],
                                                    [get_followers_ids, followers_limit, followers_ids, "followers"]]:
            if limit == 0:
                continue

            cursor = -1
            while cursor != 0:
                if screen_name:
                    response = twitter_api_func(screen_name=screen_name, cursor=cursor)
                else:
                    response = twitter_api_func(user_id=user_id, cursor=cursor)

                if response is not None:
                    ids += response['ids']
                    cursor = response['next_cursor']

                if len(ids) >= limit or response is None:
                    break
        return friends_ids[:friends_limit], followers_ids[:followers_limit]
