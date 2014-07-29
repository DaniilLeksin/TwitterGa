import tweepy
from tweepy import *

# # these tokens are necessary for user authentication
consumer_key = "OeutaQO5sAmMOmfFmnI18ghlq"
consumer_secret = "5Lta4IRxHTGHFnqmvGw9V6NCXcOhv4fAFH7dWjhmEFgtq5CD4r"
access_token = "169212559-5aMUDzIzOs0ypwQA524Xs6GjatJrUyeohRPxDiXK"
access_token_secret = "d38slbAQvii0frTx91jAWLioEFCh3AQAqnXvgppOL1a01"

class StdOutListener(StreamListener):
    ''' Handles data received from the stream. '''

    def on_status(self, status):
        # Prints the text of the tweet
        print('Tweet text: ' + status.text)

        # There are many options in the status object,
        # hashtags can be very easily accessed.
        for hashtag in status.entries['hashtags']:
            print(hashtag['text'])

        return True

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True  # To continue listening

    def on_timeout(self):
        print('Timeout...')
        return True  # To continue listening

if __name__ == '__main__':
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, listener)
    stream.filter(follow=["169212559"], track=['#test1'])

    #t = Twitter(
#        auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
#                   CONSUMER_KEY, CONSUMER_SECRET))
