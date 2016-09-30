from google.appengine.api import urlfetch

from malcat.parse import selectively_parse
from malcat.cache import server_cache


class MALScraper(object):
    API_URL = 'https://myanimelist.net/malappinfo.php'
    USER_URL = API_URL + '?u={username}&type={list_type}&status=all'

    @classmethod
    @server_cache(expire=900)
    def get_user(cls, username, list_type):
        url = cls.USER_URL.format(username=username, list_type=list_type)
        try:
            result = urlfetch.fetch(url)
        except urlfetch.Error as e:
            raise e
        else:
            return result.content

    @classmethod
    def user_info(cls, username, list_type):
        xml = cls.get_user(username, list_type)
        return next(selectively_parse(xml, 'myinfo'))

    @classmethod
    def user_list(cls, username, list_type):
        xml = cls.get_user(username, list_type)
        return selectively_parse(xml, list_type.lower())
