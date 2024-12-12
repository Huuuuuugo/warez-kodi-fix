# -*- coding: utf-8 -*-
try:
    from kodi_helper import quote_plus, urlencode, requests, json as json_
except ImportError:
    import requests
    import json as json_
    from urllib.parse import quote_plus, urlencode

URL_PROXY_CHECK = 'https://oneplayhd.com/'
URL_GET = 'https://oneplayhd.com/addon_oneplay/proxy/thunder_proxy/proxy_get.php'
URL_POST = 'https://oneplayhd.com/addon_oneplay/proxy/thunder_proxy/proxy_post.php'
URL_POST_JSON = 'https://oneplayhd.com/addon_oneplay/proxy/thunder_proxy/proxy_post_json.php'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

class unblock:
    @staticmethod
    def check_domain_proxy():
        OK = False
        try:
            r = requests.head(URL_PROXY_CHECK)
            if r.status_code == 200:
                OK = True
        except:
            pass
        return OK


    @staticmethod
    def get(url,headers={},timeout=None,allow_redirects=True):
        if headers == {}:
            headers = {'User-Agent': USER_AGENT}
        if unblock.check_domain_proxy():
            url = '{0}/?url={1}'.format(URL_GET,quote_plus(url))
        if timeout:
            r = requests.get(url,headers=headers,timeout=timeout,allow_redirects=allow_redirects)
        else:
            r = requests.get(url,headers=headers,allow_redirects=allow_redirects)
        return r

    @staticmethod
    def post(url,headers={},data=None,json=None,allow_redirects=True):
        if headers == {}:
            headers = {'User-Agent': USER_AGENT}
        if data:
            if unblock.check_domain_proxy():
                post_data = {
                    'url': url,
                    'post_params': urlencode(data)
                }
                r = requests.post(URL_POST,headers=headers,data=post_data,allow_redirects=allow_redirects)
            else:
                r = requests.post(url,headers=headers,data=data,allow_redirects=allow_redirects)
            return r
        elif json:
            if unblock.check_domain_proxy():
                post_data = {
                    'url': url,
                    'json': json_.dumps(json)
                }
                r = requests.post(URL_POST_JSON,headers=headers,data=post_data,allow_redirects=allow_redirects)
            else:
                r = requests.post(url,headers=headers,data=post_data,allow_redirects=allow_redirects)
            return r
        return