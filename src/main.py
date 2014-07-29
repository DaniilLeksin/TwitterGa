#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-oauth-post
#  - posts a status message to your timeline
#-----------------------------------------------------------------------

# from twitter import *
#
# # what should our new status be?
# new_status = "testing testing 1"
#
# # these tokens are necessary for user authentication
# # (created within the twitter developer API pages)
# consumer_key = "gBdxeNmyDbxCjFKh6mBi6onEU"
# consumer_secret = "xYYljAAmgthg3tmIiTIGFbs892mYjxlQJnxlcLnsbE7KtyQC1B"
# access_key = "169212559-5aMUDzIzOs0ypwQA524Xs6GjatJrUyeohRPxDiXK"
# access_secret = "d38slbAQvii0frTx91jAWLioEFCh3AQAqnXvgppOL1a01"
#
# # create twitter API object
# #auth = OAuth(access_key, access_secret, consumer_key, consumer_secret)
# twitter = Twitter(auth=OAuth(access_key, access_secret, consumer_key, consumer_secret))
#
# # post a new status
# # twitter API docs: https://dev.twitter.com/docs/api/1/post/statuses/update
# results = twitter.statuses.update(status=new_status)
# print "updated status: %s" % new_status
#
# #t = Twitter(
# #        auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
# #                   CONSUMER_KEY, CONSUMER_SECRET))

from api.ga_api import BigTwitterBrother

if __name__ == '__main__':
    twt = BigTwitterBrother(twitter_name="DanilLeksin")
    api = twt.get_api()
    data = twt.get_profile(api)
    friends_ids, followers_ids = twt.get_ffi(api, screen_name="DanilLeksin", friends_limit=100, followers_limit=100)
    print "friends: %s\nfollowers: %s" % (friends_ids, followers_ids)