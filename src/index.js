var cheerio = require('cheerio');
var fs = require('fs');
var {URL} = require('url')
var genEpub = require('gen-epub')
var crypto = require('crypto');
var iconv = require('iconv-lite')
var config = require('./config.js')
var processImg = require('./img.js')
var {requestRetry, sleep} = require('./util.js');

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

function getTocFromCfg() {
    
    if(config.list && config.list.length > 0)
        return config.list;
    
    if (!config.url) {
        console.log('URL not specified')
        process.exit()
    }
    
    var html = requestRetry('GET', config.url, {
        retry: config.retry,
        headers: config.headers,
        timeout: config.timeout * 1000,
    }).body
    html = iconv.decode(html, config.encoding)
    var toc = getToc(html);
    return toc;
    
}

function getToc(html)  {
        
    var $ = cheerio.load(html);
    
    if(config.remove)
        $(config.remove).remove()
    
    var $links = $(config.link);
    var vis = new Set()

    var res = [];
    for(var i = 0; i < $links.length; i++)
    {
        var $link = $links.eq(i)
        var url = $link.attr('href');
        if(!url) {
            var text = $link.text()
            res.push(text)
            continue
        }
        
        url = url.replace(/#.*$/, '')
        if(config.base)
            url = new URL(url, config.base).toString()
        if(vis.has(url)) continue
        vis.add(url)
        res.push(url)
    }
    return res;
}

function getArticle(html, url) {
    
    var $ = cheerio.load(html);
    
    if(config.remove)
        $(config.remove).remove()
    
    // 只取一个元素
    var $title = $(config.title).eq(0)
    var title = $title.text().trim()
    $title.remove()
    
    // 解决 Cheerio 的 .html 多播问题
    var $co = $(config.content)
    var co = []
    for(var i = 0; i < $co.length; i++)
        co.push($co.eq(i).html())
    co = co.join('\r\n')

    if(config.credit) {
        var credit = `<blockquote>原文：<a href='${url}'>${url}</a></blockquote>`
        co = credit + co
    }
    
    return {title: title, content: co}
}

function main() {
    
    var configFname = process.argv[2] || 'config.json'
    if(!fs.existsSync(configFname)) {
        console.log('please provide config file')
        return
    }
    var userConfig = JSON.parse(fs.readFileSync(configFname, 'utf-8'))
    Object.assign(config, userConfig)
    
    var toc = getTocFromCfg()
    
    var articles = []
    var imgs = new Map()
    
    if(config.name) {
        articles.push({
            title: config.name, 
            content: `<p>来源：<a href='${config.url}'>${config.url}</a></p>`
        })
    }

    for(var url of toc) {
        try {
            console.log('page: ' + url);
            
            if(url.startsWith('http')) {
                var html = requestRetry('GET', url, {
                    headers: config.headers,
                    retry: config.retry,
                    timeout: config.timeout * 1000,
                }).body
                html = iconv.decode(html, config.encoding)
                var art = getArticle(html, url)
                art.content = processImg(art.content, imgs, {
                    pageUrl: url, 
                    imgPrefix: '../Images/'
                })
                articles.push(art)
                sleep(config.wait)
            } else 
                articles.push({title: url, content: ''})
            
        } catch(ex) {console.log(ex)}
    }
    
    genEpub(articles, imgs)
    console.log('done...');
}

if(module == require.main) main()