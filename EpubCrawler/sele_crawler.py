from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from GenEpub import gen_epub
from urllib.parse import urljoin
import sys
import json
import re
import hashlib
import base64
import time
from concurrent.futures import ThreadPoolExecutor
import threading
import traceback
from .util import *
from .img import process_img
from .config import config
from .common import *

trlocal = threading.local()
drivers = []

JS_GET_IMG_B64 = '''
function getImageBase64(img_stor) {
    var img = document.querySelector(img_stor)
    if (!img) return ''
    var canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, img.width, img.height);
    var dataURL = canvas.toDataURL("image/png");
    return dataURL;
}
'''

'''
def get_img_src(el_img):
    url = ''
    for prop in config['imgSrc']:
        url = el_img.attr(prop)
        if url: break
    return url
    
    
def process_img_data_url(url, el_img, imgs, **kw):
    if not re.search(RE_DATA_URL, url):
        return False
    picname = hashlib.md5(url.encode('utf-8')).hexdigest() + '.png'
    print(f'pic: {url} => {picname}')
    if picname not in imgs:
        enco_data = re.sub(RE_DATA_URL, '', url)
        data = base64.b64decode(enco_data.encode('utf-8'))
        data = opti_img(data, config['optiMode'], config['colors'])
        imgs[picname] = data
    el_img.attr('src', kw['img_prefix'] + picname)
    return True
    
def process_img(driver, html, imgs, **kw):
    kw.setdefault('img_prefix', 'img/')
    
    root = pq(html)
    el_imgs = root('img')
    
    for i in range(len(el_imgs)):
        el_img = el_imgs.eq(i)
        url = get_img_src(el_img)
        if not url: continue
        if process_img_data_url(url, el_img, imgs, **kw):
            continue
        if not url.startswith('http'):
            if kw.get('page_url'):
                url = urljoin(kw.get('page_url'), url)
            else: continue
        
        picname = hashlib.md5(url.encode('utf-8')).hexdigest() + '.png'
        print(f'pic: {url} => {picname}')
        if picname not in imgs:
            try:
                driver.get(url)
                b64 = driver.execute_script(
                    JS_GET_IMG_B64 + '\nreturn getImageBase64("body>img")')
                print(b64[:100])
                process_img_data_url(b64, el_img, imgs, **kw)
                time.sleep(config['wait'])
            except Exception as ex: print(ex)
        
    return root.html()
'''

def wait_content_cb(driver):
    return driver.execute_script('''
        var titlePresent = document.querySelector(arguments[0]) != null
        var contPresent = document.querySelector(arguments[1]) != null
        return titlePresent && contPresent
    ''', config['title'], config['content'])

def download_page(url, art, imgs):
    print(url)
    
    if not hasattr(trlocal, 'driver'):
        trlocal.driver = create_driver()
        drivers.append(trlocal.driver)
    driver = trlocal.driver
    
    if not re.search(r'^https?://', url):
        articles.append({'title': url, 'content': ''})
        return
    driver.get(url)
    # 显式等待
    if config['waitContent']:
        WebDriverWait(driver, config['waitContent'], 0.5) \
            .until(wait_content_cb, "无法获取标题或内容")
    html = driver.find_element_by_css_selector('body').get_attribute('outerHTML')
    art.update(get_article(html, url))
    art['content'] = process_img(art['content'], imgs, page_url=url, img_prefix='../Images/')
    time.sleep(config['wait'])

def download_page_safe(url, art, imgs):
    try: download_page(url, art, imgs)
    except: traceback.print_exc()

def create_driver():
    options = Options()
    if not config['debug']:
        options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)
    driver.get(config['url'])
    
    for kv in config.get('headers', {}).get('Cookie', '').split('; '):
        kv = kv.split('=')
        if len(kv) < 2: continue
        driver.add_cookie({'name': kv[0], 'value': kv[1]})
    driver.get(config['url'])
    
    return driver
    
def crawl_sele():
    articles = [{
        'title': config['name'],
        'content': f"<p>来源：<a href='" + config['url'] + "'>" + config['url'] + "</a></p>"
    }]
    imgs = {}
    pool = ThreadPoolExecutor(config['textThreads'])
    hdls = []
    for url in config['list']:
        art = {}
        articles.append(art)
        h = pool.submit(download_page_safe, url, art, imgs)
        hdls.append(h)
        # download_page_safe(driver, url, articles, imgs)
    for h in hdls: h.result()
    
    articles = [art for art in articles if art]
    gen_epub(articles, imgs)
    
    for d in drivers: d.close()
