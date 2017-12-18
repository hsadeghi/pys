import tweepy
from tweepy import OAuthHandler
import json
def main():
    consumer_key = 'SAX3xOqAm9Ael33f13Y3AqOAc'
    consumer_secret = 'r89YtPqu7cFjs9QcsCLCdqn8ohTnT9BOQdETY0r3S8jyHOYBYm'
    access_token = '863154728343089153-9QukaXIbCq4LNXbphuA2U3Mxb9lz6FJ'
    access_secret = 'AOaLAmGqUrTEImpu3JeNBDlqcNqUKXPoWNZPV4lSrgsd6'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    twt = tweepy.API(auth)

    for newTw in tweepy.Cursor(twt.home_timeline).items(4):
        #newTw. ??? status._json
        print json.dumps(newTw._json)

    jsdata = '{ "name": ["hadi", "sadeghi", "taheri"], "email" : "hadi.sad3ghi@gmail.com", "public": "no", "phone" : ' \
             '{"home" : "none" , "mobile" : "+32491326841"} }'
    inf = json.loads(jsdata)
    print 'full name : ', inf['name']
    print 'contact: ', inf['phone']['mobile']
    #res = ''
    print processJson(inf)


def processJson(jsn, res = '' ):
    if isinstance(jsn, basestring):
        res = res + '\t' + jsn
        return res
    if isinstance(jsn, dict):
        for key,val in jsn.items():
            res = res + '\n'+key + ': '
            res += processJson(val)
        return res
    if isinstance(jsn, list):
        for item in jsn:
            res += processJson(item)
        return res
    #res = res + jsn
    return res

if __name__ == '__main__':
    main()


