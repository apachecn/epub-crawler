import re
from pyquery import PyQuery as pq
from .config import config
from readability import Document

def get_article(html, url):
    # 预处理掉 XML 声明和命名空间
    html = re.sub(r'<\?xml[^>]*\?>', '', html)
    html = re.sub(r'xmlns=".+?"', '', html)
    root = pq(html)
    
    if config['remove']:
        root(config['remove']).remove()
        
    el_title = root(config['title']).eq(0)
    title = el_title.text().strip()
    el_title.remove()
    
    if config['content']:
        el_co = root(config['content'])
        co = '\r\n'.join([
            el_co.eq(i).html()
            for i in range(len(el_co))
        ])
    else:
        co = Document(str(root)).summary()
        co = pq(co).find('body').html()
    
    if config['credit']:
        credit = f"<blockquote>原文：<a href='{url}'>{url}</a></blockquote>"
        co = credit + co
        
    return {'title': title, 'content': co}