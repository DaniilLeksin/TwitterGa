#!/usr/bin/python

from api.ga_api import BigTwitterBrother
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        print "Input twitter name as the first argument"
        exit(0)
    twt = BigTwitterBrother(twitter_name=name)
    api = twt.get_api()
    response = twt.make_request(api.users.lookup, screen_name=name)
    if response:
        print "name: %s" % response[0]['name']
        print "id_str: %s" % response[0]['id_str']
        print "created_at: %s" % response[0]['created_at']
        print "profile_image_url: %s" % response[0]['profile_image_url']
        print "time_zone: %s" % response[0]['time_zone']
        print "utc_offset: %s" % response[0]['utc_offset']
        print "------------------------------------------"
        print "total twt: %s" % response[0]['statuses_count']
        print "last tweet: %s" % response[0]['status']['text']
        print "------------------------------------------"
    data = twt.get_profile(api)
    friends_ids, followers_ids = twt.get_ffi(api, screen_name=name, friends_limit=100, followers_limit=100)
    print "friends: (%d)%s\n---------------------------------\nfollowers (%d): %s" % (len(friends_ids), friends_ids, len(followers_ids), followers_ids)
