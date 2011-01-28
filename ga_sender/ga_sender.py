#!/usr/bin/env python
# -*- coding: UTF-8 -*-r

import sys
import uuid
import socket
import httplib2
import time
from urllib import quote 
from random import randint

class GoogleAnlayticsMobile(object):
    __utma = None
    __utma_c_time = 63072000
    __utmb = None
    __utmb_c_time = 1800
    __utmc = None
    __utmz = ''
    __utmz_c_time = 604800

    ga_utmhn = None
    ga_utmac = None
    ga_utmwv = '4.3.1'
    ga_hash = 0
    ga_img = 'http://www.google-analytics.com/__utm.gif'
    ga_search = [['google', 'q'], ['yahoo', 'p']]

    ga_referer = None
    time = None
    html = None

    img_url = None

    def __init__(self, ga_utmac, ga_utmhn, env, uri=None, ga_params=[]):
        self.ga_utmac = ga_utmac
        self.ga_utmhn = ga_utmhn
        self.ga_hash = self.gen_hash(ga_utmhn)

        self.time = self.gen_time()
        
        if uri is None:
            uri = env.get('uri')
        self.ga_referer = env.get('referer')
        source = self.get_traffic_source(env)
        source_str = ''
        if source.get('utmgclid'):
            source_str = 'utmgclid=' + source.get('utmgclid')
        else:
            source_str = 'utmcsr=' + source['utmcsr']
        source_str = (source_str + '|utmccn=' + source.get('utmccn') +
            '|utmcmd=' + source.get('utmcmd'))
        if source.get('utmctr'):
            source_str = source_str + '|utmctr=' + source.get('utmctr')
        if source.get('utmctt'):
            source_str = soucce_str + '|utmcct=' + source.get('utmcct')

        c_id = ('%f' % ((randint(1000000000, 2147483647) ^ self.ga_hash) *2147483647))
        c_id = str(c_id).split('.')
        self.__utma = str(self.ga_hash) + '.' + str(c_id[0]) + '.' + self.time + '.' + self.time + '.' + self.time + '.1'
        self.__utmb = str(self.ga_hash) + '.1.10.' + self.time
        self.__utmc = str(self.ga_hash)
        self.__utmz = str(self.ga_hash) + '.' + self.time + '.1.1.' + source_str
        utmz = quote(self.__utmz)
        self.img_url = str(self.ga_img) + '?utmwv=' + self.ga_utmwv + \
            '&utmn=' + str(randint(1000000000, 9999999999)) + '&utmhn=' + \
            self.ga_utmhn + '&utmhid=' + str(randint(1000000000, 9999999999)) + \
            '&utmr=' + quote(env.get('referer') or '-') + \
            '&utmp=' + quote(env.get('url')) + \
            '&utmac=' + self.ga_utmac + '&utmcc=__utma%3D' + self.__utma + \
            '%3B%2B__utmz%3D' + utmz + '%3B'

    def gen_hash(self, ga_utmhn):
        if not ga_utmhn:
            return 1
        h, g = 0, 0
        i = len(ga_utmhn) - 1
        while i >=0:
            c = int(ord(ga_utmhn[i]))
            h = ((h << 6) & 0xfffffff) + c + (c << 14)
            g = (h & 0xfe00000)
            if g:
                h = (h ^ (g >> 21))
            i = i - 1
        return h

    def gen_time(self):
        return str(time.time()).split('.')[0]

    def get_traffic_source(self, env):
        if env.get('utm_source') and env.get('utm_medium'):
            utmccn = env.get('utm_campaign') if env.get('utm_campaign') else '(not set)'
            utmcct = env.get('utm_content') if env.get('utm_content') else '(not set)'
            return dict(utmgclid='', utmcsr=env.get('utm_source',''), utmccn=utmccn, utmctr=env.get('utm_term',''), utmcct=utmcct)
        elif self.ga_referer:
            return dict(utmgclid='', utmcsr='(direct)', utmccn='(direct)', utmcmd='(none)', utmctr='', utmcct='')
        return dict(utmgclid='', utmcsr='(direct)', utmccn='(direct)', utmcmd='(none)', utmctr='', utmcct='')

    def get_imgurl(self):
        return self.img_url

def send_request_to_google_analytics(utm_url, environ):
    http = httplib2.Http()    
    try:
        resp, content = http.request(utm_url, 
            'GET', 
            headers={'User-Agent': environ.get('user_agent', 'Unknown')}
        )
        socket.setdefaulttimeout(10)
        if resp.get('status') != '200':
            print resp
        else:
            print '%s Sended' % environ.get('ip')
            #print utm_url
            pass
    except:
        pass

def send_to_ga(environ):
    g = GoogleAnlayticsMobile('UA-15296817-5', 'www.jguoer.com', environ)
    send_request_to_google_analytics(g.get_imgurl(), environ)

e = {'domain': 'www.jguoer.com', 'protocol': 'HTTP/1.1', 'uid': '39454209', 'status_code': '200', 'url': '/?session=3fd90546_39454209', 'ip': '122.192.166.136', 'bid': '4979797d', 'time': '2011-1-28 14:40:35 +0800', 'page_size': '3821', 'referer': 'http://www.jguoer.com/?session=6acf607a_39454209', 'user_agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; zh-cn) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7', 'process_time': '0', 'method': 'GET'}
send_to_ga(e)
