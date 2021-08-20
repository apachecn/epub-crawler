# -*- coding: utf-8 -*-

import requests
from imgyaso import pngquant_bts, \
    adathres_bts, grid_bts, noise_bts, trunc_bts

def request_retry(method, url, retry=10, **kw):
    kw.setdefault('timeout', 10)
    for i in range(retry):
        try:
            return requests.request(method, url, **kw)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print(f'{url} retry {i}')
            if i == retry - 1: raise e
            
def opti_img(img, mode, colors):
    if mode == 'quant':
        return pngquant_bts(img, colors)
    elif mode == 'grid':
        return grid_bts(img)
    elif mode == 'trunc':
        return trunc_bts(img, colors)
    elif mode == 'thres':
        return adathres_bts(img)
    else:
        return img