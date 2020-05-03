var request = require('sync-request');
var chp = require('child_process')

var isDir = s => fs.statSync(s).isDirectory()

var isPic = x => x.endsWith('.jpg') || 
                 x.endsWith('.jpeg') || 
                 x.endsWith('.png') || 
                 x.endsWith('.gif') ||  
                 x.endsWith('.tiff') ||  
                 x.endsWith('.bmp') ||  
                 x.endsWith('.webp')

function safeMkdir(dir) {
    try {fs.mkdirSync(dir)}
    catch(ex) {}
}

function safeUnlink(f){
    try {fs.unlinkSync(f)}
    catch(ex) {}
}

function requestRetry(method, url, options={}) {
    
    options.retry = options.retry || 5
    options.timeout = options.timeout || 4000
    options.socketTimeout = options.socketTimeout || 4000
    
    for(var i = 0; i < options.retry; i++) {
        try {
            return request(method, url, options)
        } catch(ex) {
            if(i == options.retry - 1) throw ex;
        }
    }
}

function sleep(sec) {
    chp.spawnSync('sleep', [sec])
}

function optiImg(img, mode='quant', colors=8) {
    if(mode == 'none')
        return img
    var fname = path.join(
        os.tmpdir(), 
        uuid.v4() + '.png'
    )
    fs.writeFileSync(fname, img)
    chp.spawnSync('imgyaso', [fname, '-m', mode, '-c', 8])
    img = fs.readFileSync(fname)
    safeUnlink(fname)
    return img
}

exports.requestRetry = requestRetry
exports.isDir = isDir
exports.isPic = isPic
exports.safeMkdir = safeMkdir
exports.safeUnlink = safeUnlink
exports.sleep = sleep
exports.optiImg = optiImg