#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" Refer to the document of twitter API.
https://dev.twitter.com/rest/reference/post/statuses/update
"""

import requests
from requests_oauthlib import OAuth1Session

class Twitter(object):
    """ Base class to tweet on twitter.
    """
    _url_api = "https://api.twitter.com/1.1/statuses/update.json"

    def __init__(self, consumer_key, consumer_sec, access_tok, access_sec):
        """ Initialize class object with necessary keys to access twitter.

        Args:
            consumer_key (str) : Consumer key
            consumer_sec (str) : Consumer secret
            access_tok (str) : Access token
            access_sec (str) : Access token secret

        Returns:
            None
        """
        self._twitter = OAuth1Session(consumer_key, consumer_sec, access_tok, access_sec)

    def tweet(self, message):
        """ Tweet with the specified message.

        Args:
            message (str) : message to post

        Returns:
            True if succeeded.
        """
        params = {"status":message}
        req = self._twitter.post(self._url_api, params=params)

        return True if req.status_code == 200 else False

if __name__ == "__main__":
    import sys
    my_twitter = Twitter(\
            "", \
            "", \
            "", \
            "")

    my_twitter.tweet(sys.argv[1])

