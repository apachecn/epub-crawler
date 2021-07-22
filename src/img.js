#!/usr/bin/env node

var chp = require('child_process')
var fs = require('fs');
var os = require('os')
var crypto = require('crypto');
var {Command} = require('commander');
var cheerio = require('cheerio');
var path = require('path')
var uuid = require('uuid')
var config = require('./config.js')
var pkg = require('../package.json');
var {
    requestRetry, 
    isDir, 
    safeMkdir,
    safeUnlink,
    sleep,
    optiImg,
} = require('./util.js')

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

function processDir(dir) {
    var files = fs.readdirSync(dir);
    for(var fname of files) {
        fname = path.join(dir, fname)
        processFile(fname)
    }
}

function processFile(fname) {
    if(!fname.endsWith('.html') &&
       !fname.endsWith('.md'))
        return;
    console.log('file: ' + fname);
    var content = fs.readFileSync(fname, 'utf-8');
    var imgs = new Map()
    if(fname.endsWith('.html'))
        content = processImg(content, imgs);
    else
        content = processImgMd(content, imgs);
    fs.writeFileSync(fname, content);
    var dir = path.join(path.dirname(fname), 'img')
    for(var [fname, img] of imgs.entries()) {
        fs.writeFileSync(path.join(dir, fname), img)
    }
}

function processImgMd(md, imgs, options={}) {
    options.imgPrefix = options.imgPrefix || 'img/'
    
    var re = /!\[.*?\]\((.*?)\)/g
    var rm;
    while(rm = re.exec(md)) {
        try {
            var url = rm[1]
            if(!url) continue
            if(options.pageUrl)
                url = new URL(url, options.pageUrl).toString()
            if(!url.startsWith('http')) continue
            url = encodeURI(url).replace(/%25/g, '%')
            
            var picname = crypto.createHash('md5').update(url).digest('hex') + ".png";
            console.log(`pic: ${url} => ${picname}`)
            
            if(!imgs.has(picname)) {
                var data = requestRetry('GET', url, {
                    headers: config.headers,
                    retry: config.retry,
                    timeout: config.timeout * 1000,
                }).body
                data = optiImg(data, config.optiMode, config.colors)
                imgs.set(picname, data);
                sleep(config.wait)
            }
            
            md = md.split(rm[1]).join(options.imgPrefix + picname)
        } catch(ex) {console.log(ex.toString())}
    }
    
    return md
}

function getImgSrc($img) {
	var url = ''
	for(var prop of config.imgSrc) {
		url = $img.attr(prop)
		if(url) break
	}
	return url
	
}

function processImg(html, imgs, options={}) {
    
    options.imgPrefix = options.imgPrefix || 'img/'
    
    var $ = cheerio.load(html);
    
    var $imgs = $('img');

    for(var i = 0; i < $imgs.length; i++) {
        try {
            var $img = $imgs.eq(i);
            var url = getImgSrc($img)
            if(!url) continue
            if(!url.startsWith('http')) {
                if(options.pageUrl)
                    url = new URL(url, options.pageUrl).toString()
                else
                    continue
            }
            url = encodeURI(url).replace(/%25/g, '%')
            
            var picname = crypto.createHash('md5').update(url).digest('hex') + ".png";
            console.log(`pic: ${url} => ${picname}`)
            
            if(!imgs.has(picname)) {
                var data = requestRetry('GET', url, {
                    headers: config.headers,
                    retry: config.retry,
                    timeout: config.timeout * 1000,
                }).body
                data = optiImg(data, config.optiMode, config.colors)
                imgs.set(picname, data);
                sleep(config.wait)
            }
            
            $img.attr('src', options.imgPrefix + picname);
        } catch(ex) {console.log(ex.toString())}
    }
    
    return $.html();
}

function main() {
    
    var cmder = new Command()
    cmder.name('crawl-img')
         .version(pkg.version)
         .arguments('<fname>', 'img file name of dir name')
         .option('-r, --retry <retry>', 'time of retrying', parseInt, 10)
         .option('-w, --wait <wait>', 'wait time in seconds', parseFloat, 0)
         .option('-m, --opti-mode <mode>', 'image optimization mode', 'quant')
         .option('-c, --colors <colors>', 'num of colors for image optimization mode', parseInt, 8)
         .option('-t, --timeout <timeout>', 'timeout', parseInt, 8)
    args = cmder.parse()
    
    config.retry = args.retry
    config.wait = args.wait
    config.optiMode = args.optiMode
    config.colors = args.colors
    config.timeout = args.timeout
    
    var fname = args.args[0]
    if(!fs.existsSync(fname))
    {
        console.log('file or dir not found');
        return
    }
    
    if(isDir(fname)) {
        safeMkdir(path.join(fname, 'img'))
        processDir(fname)
    } else {
        safeMkdir(path.join(path.dirname(fname), 'img'))
        processFile(fname)
    }
}

module.exports = processImg

if(module == require.main) main();