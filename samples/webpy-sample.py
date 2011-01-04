#!/usr/bin/env python

import web
from urllib import urlencode
from random import randint

urls = (
    '/', 'index',
    '/index', 'index'
)

#URL is image server url
IMAGE_URL = 'http://127.0.0.1:9090/'

GA_ACCOUNT = 'UA-15296817-1'

def gen_url():
    referer = web.ctx.env.get('HTTP_REFERER')
    query = web.ctx.env.get('QUERY_STRING')
    path = web.ctx.env.get('REQUEST_URI')

    referer = '-' if not referer else urlencode(referer)
    path = '&utmp=%s' % urlencode(path) if path else ''

    url = ('%s?utmac=%s&utmn=%s&utmr=%s%s&guid=%s' %
        (IMAGE_URL, GA_ACCOUNT, randint(0, 0x7fffffff), referer,
        path, 'ON'))
    return url

class index:
    def GET(self):
        url = gen_url()
        html = """
            <html>
                <head>
                    <title>
                        Test Mobile GA Python
                    </title>
                </head>
                <body>
                    This is test image:
                    <img src="%s"/> <br/>
                    %s
                </body>
            </html>
        """ % (url, url)
        return html

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
