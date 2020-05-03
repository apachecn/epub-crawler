var cheerio = require('cheerio');

// for sphinx docs
function processDecl(html) {
    
    var $ = cheerio.load(html)
    $('colgroup').remove()
    
    var $dts = $('dt')
    
    for(var i = 0; i < $dts.length; i++) {
        var $dt = $dts.eq(i)
        $dt.find('a.reference').remove()
        var t = $dt.text()
        var $pre = $('<pre></pre>')
        $pre.text(t)
        $dt.replaceWith($pre)
    }
    
    return $.html()
}

function processMath(html){
    
    var $ = cheerio.load(html)
    
    var $maths = $('span.math, div.math');
    for(var i = 0; i < $maths.length; i++) {
        var $m = $maths.eq(i)
        var tex = $m.text().replace(/\\\[|\\\]|\\\(|\\\)/g, '')
        var url = 'http://latex.codecogs.com/gif.latex?' + encodeURIComponent(tex)
        var $img = $('<img />')
        $img.attr('src', url)
        if($m.is('div')) {
            var $p = $('<p></p>')
            $p.append($img)
            $img = $p
        }
        $m.replaceWith($img)
    }
    
    return $.html()
}
