# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, quote_plus
import hashlib
from pyquery import PyQuery as pq
import time
from .util import *
from .config import config

img_pool = ThreadPoolExecutor(5)

def set_img_pool(pool):
    global img_pool
    img_pool = pool
    
def get_img_src(el_img):
    url = ''
    for prop in config['imgSrc']:
        url = el_img.attr(prop)
        if url: break
    return url
    
def tr_download_img(url, imgs, picname):
    try:
        data = request_retry(
            'GET', url,
            headers=config['headers'],
            retry=config['retry'],
            timeout=config['timeout'],
            proxies=config['proxy'],
        ).content
        data = opti_img(data, config['optiMode'], config['colors'])
        imgs[picname] = data or b''
        time.sleep(config['wait'])
    except Exception as ex:
        print(ex)
    
def process_img(html, imgs, **kw):
    kw.setdefault('img_prefix', 'img/')
    
    root = pq(html)
    el_imgs = root('img')
    hdls = []
    
    for i in range(len(el_imgs)):
        el_img = el_imgs.eq(i)
        url = get_img_src(el_img)
        if not url: continue
        if not url.startswith('http'):
            if kw.get('page_url'):
                url = urljoin(kw.get('page_url'), url)
            else: continue
        
        picname = hashlib.md5(url.encode('utf-8')).hexdigest() + '.png'
        print(f'pic: {url} => {picname}')
        if picname not in imgs:
            hdl = img_pool.submit(tr_download_img, url, imgs, picname)
            hdls.append(hdl)
            
        el_img.attr('src', kw['img_prefix'] + picname)
        el_img.attr('data-original-src', url)
        
    for h in hdls: h.result()
    return root.html()
    
    