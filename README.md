# epub-crawler

用于抓取网页内容并制作 EPUB 的小工具。

## 安装

通过 pip（推荐）：

```
pip install EpubCrawler
```

从源码安装：

```
pip install git+https://github.com/apachecn/epub-crawler
```

## 使用指南

```
crawl-epub [CONFIG]

CONFIG: JSON 格式的配置文件，默认为当前工作目录中的 config.json
```

配置文件包含以下属性：

+   `name: String`
    
    元信息中的书籍名称，也是在当前工作目录中保存文件的名称
    
+   `url: String`（可空）

    目录页面的 URL
    
+   `link: String`（可空）

    链接`<a>`的选择器
    
+   `list: [String]`（可空）

    待抓取页面的列表，如果这个列表不为空，则抓取这个列表，忽略`url`和`link`
    
+   `title: String`

    文章页面的标题选择器
    
+   `content: String`

    文章页面的内容选择器

+   `remove: String`（可空）

    文章页面需要移除的元素的选择器
    
+   `credit: Boolean`（可空）

    是否显示原文链接
    
+   `headers: {String: String}`（可空）

    HTTP 请求的协议头，默认为`{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}`
    
+   `retry: Integer`（可空）

    HTTP 请求的重试次数，默认为 10
    
+   `wait: Float`（可空）

    两次请求之间的间隔（秒），默认为 0
    
+   `timeout: Integer`（可空）

    HTTP 请求的超时（秒），默认为 8
    
+   `encoding: String`（可空）

    网页编码，默认为 UTF-8
    
+   `optiMode: String`（可空）

    图片处理的模型，`'none'`表示不处理，其它值请见 imgyaso 支持的模式，默认为`'quant'`
    
+   `colors: Integer`（可空）

    imgyaso 接收的`colors`参数，默认为 8
	
+   `imgSrc: [String]`（可空）

    图片源的属性，默认为`["data-src", "data-original-src", "src"]`
	
+   `proxy: String`（可空）

    要使用的索引，格式为`<protocal>://<host>:<port>`
	
+   `textThreads: Integer`（可空）

    爬取文本的线程数，默认为 5
	
+   `imgThreads: Integer`（可空）

    爬取图片的线程数，默认为 5

用于抓取我们的 PyTorch 1.4 文档的示例：

```json
{
    "name": "PyTorch 1.4 中文文档 & 教程",
    "url": "https://gitee.com/apachecn/pytorch-doc-zh/blob/master/docs/1.4/SUMMARY.md",
    "link": ".markdown-body li a",
    "title": ".markdown-body>h1",
    "content": ".markdown-body",
    "remove": "a.anchor",
}
```

## 协议

本项目基于 SATA 协议发布。

您有义务为此开源项目点赞，并考虑额外给予作者适当的奖励。

## 赞助我们

![](https://home.apachecn.org/img/about/donate.jpg)

## 另见

+   [ApacheCN 学习资源](https://docs.apachecn.org/)
+   [计算机电子书](http://it-ebooks.flygon.net)
+   [布客新知](http://flygon.net/ixinzhi/)
