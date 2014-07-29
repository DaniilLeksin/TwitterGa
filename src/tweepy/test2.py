import sys
import time
from urllib2 import URLError

from functools import partial
from sys import maxint 
import json
import twitter
 
def oauth_login():
 
    CONSUMER_KEY='OeutaQO5sAmMOmfFmnI18ghlq'
    CONSUMER_SECRET='5Lta4IRxHTGHFnqmvGw9V6NCXcOhv4fAFH7dWjhmEFgtq5CD4r'
    OAUTH_TOKEN='169212559-5aMUDzIzOs0ypwQA524Xs6GjatJrUyeohRPxDiXK'
    OAUTH_TOKEN_SECRET='d38slbAQvii0frTx91jAWLioEFCh3AQAqnXvgppOL1a01'
 
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
 
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api
 
def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw):
 
 
        def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
 
                if wait_period > 3600:
                    print >> sys.stderr, 'Too many retries. Quitting.'
                    raise e
 
                if e.e.code ==401:
                    print >> sys.stderr, 'Encountered 401 Error (Not Authorized)'
                    return None
                elif e.e.code ==404:
                    print >> sys.stderr, 'Encountered 404 Error (Not Found)'
                    return None
                elif e.e.code ==429:
                    print >> sys.stderr, 'Encountered 429 Error (Rate Limit Exceeded)'
                    if sleep_when_rate_limited:
                        print >> sys.stderr, "Retrying in 15 minutes...ZZZ..."
                        sys.stderr.flush()
                        time.sleep(60*15 + 5)
                        print sys.stderr, '...ZZZ...Awake now and trying again.'
                        return 2
                    else:
                        raise e
                elif e.e.code in (500, 502, 503, 504):
                    print >> sys.stderr, 'Encountered %i Error . Retrying in %i seconds' %\
                          (e.e.code, wait_period)
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
 
def get_user_profile(twitter_api, screen_names=None, user_ids=None):
                assert (screen_names !=None) != (user_ids !=None), \
                "Must have screen_names or user_ids, but not both"
 
                items_to_info = {}
 
                items = screen_names or user_ids
 
                while len(items) > 0:
                    items_str = ',' .join([str(item) for item in items[:100]])
                    items = items[100:]
 
                if screen_names:
                    response = make_twitter_request(twitter_api.users.lookup, screen_name=items_str)
 
                else:
                    response = make_twitter_request(twitter_api.users.lookup, user_id=items_str)
 
                for user_info in response:
                    if screen_names:
                        items_to_info[user_info['screen_name']] = user_info
                    else:
                        items_to_info[user_info['id']] = user_info
 
                    return items_to_info
 
def get_friends_followers_ids(twitter_api, screen_name=None, user_id=None,
                              friends_limit=maxint, followers_limit=maxint):
 
    assert(screen_name != None) != (user_id != None), \
    "Must have screen_name or user_id but not both"
 
    get_friends_ids = partial(make_twitter_request, twitter_api.friends.ids,
                              count=5000)
    get_followers_ids = partial(make_twitter_request, twitter_api.followers.ids,
                                count=5000)
    friends_ids, followers_ids = [], []
 
    for twitter_api_func, limit, ids, label in [
                    [get_friends_ids, friends_limit, friends_ids, "friends"],
                    [get_followers_ids, followers_limit, followers_ids, "followers"]
                ]:
        if limit == 0: continue
 
        cursor = -1
 
        while cursor != 0:
 
            if screen_name:
                response = twitter_api_func(screen_name=screen_name, cursor=cursor)
 
            else:
                response = twitter_api_func(user_id=user_id, cursor=cursor)
 
            if response is not None:
                ids += response['ids']
                curosr = response['next_cursor']
 
            print >> sys.stderr, 'Fetched {0} total {1} ids for {2}'.format(len(ids),
                                                    label, (user_id or screen_name))
 
            if len(ids) >= limit or response is None:
                break
        return friends_ids[:friends_limit], followers_ids[:followers_limit]
 
 
        #9.16 9.17 9.19 9.22
 
twitter_api = oauth_login()
response = make_twitter_request(twitter_api.users.lookup, screen_name="DanilLeksin")
print json.dumps(response, indent=1)
print twitter_api
print get_user_profile(twitter_api, screen_names=["DanilLeksin"])
friends_ids, followers_ids = get_friends_followers_ids(twitter_api,
                                                       screen_name="DanilLeksin",
                                                       friends_limit=10,
                                                       followers_limit=100)
print friends_ids
print followers_ids
