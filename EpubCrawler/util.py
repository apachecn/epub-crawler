# -*- coding: utf-8 -*-

import requests
from imgyaso import pngquant_bts, \
    adathres_bts, grid_bts, noise_bts, trunc_bts
import os
import shutil
import tempfile
import sys
from os import path
import uuid

is_pic = lambda x: x.endswith('.jpg') or \
                   x.endswith('.jpeg') or \
                   x.endswith('.png') or \
                   x.endswith('.gif') or \
                   x.endswith('.tiff') or \
                   x.endswith('.bmp') or \
                   x.endswith('.webp')

def safe_mkdir(dir):
    try: os.mkdir(dir)
    except: pass
    
def safe_rmdir(dir):
    try: shutil.rmtree(dir)
    except: pass

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
        
def safe_remove(name):
    try: os.remove(name)
    except: pass

def load_module(fname):
    if not path.isfile(fname) or \
        not fname.endswith('.py'):
        raise FileNotFoundError('外部模块应是 *.py 文件')
    tmpdir = path.join(tempfile.gettempdir(), 'load_module')
    safe_mkdir(tmpdir)
    if tmpdir not in sys.path:
        sys.path.insert(0, tmpdir)
    mod_name = 'x' + uuid.uuid4().hex
    nfname = path.join(tmpdir, mod_name + '.py')
    shutil.copy(fname, nfname)
    mod = __import__(mod_name)
    safe_remove(nfname)
    return mod