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
    
+   `url: String`（和`list`二选一）

    目录页面的 URL
    
+   `link: String`（若`url`非空则必填）

    链接`<a>`的选择器
    
+   `list: [String]`（和`url`二选一）

    待抓取页面的列表，如果这个列表不为空，则抓取这个列表
	
	⚠该配置项会覆盖`url`、`link`和`external`⚠
    
+   `title: String`（可空）

    文章页面的标题选择器（默认为`title`）
    
+   `content: String`（可空）

    文章页面的内容选择器，为空则智能分析

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

    同时设置 HTTP 请求的连接和读取超时（秒）
    
    ⚠会覆盖`connTimeout`和`readTimeout`

+   `connTimeout: Integer`（可空）

    HTTP 请求的连接超时（秒），默认为 1

+   `readTimeout: Integer`（可空）

    HTTP 请求的读取超时（秒），默认为 60
    
+   `encoding: String`（可空）

    网页编码，默认为 UTF-8
    
+   `optiMode: String`（可空）

    图片处理的模型，`'none'`表示不处理，其它值请见 imgyaso 支持的模式，默认为`'quant'`
    
+   `colors: Integer`（可空）

    imgyaso 接收的`colors`参数，默认为 8
	
+   `imgSrc: [String]`（可空）

    图片源的属性，默认为`["data-src", "data-original-src", "src"]`
	
+   `proxy: String`（可空）

    要使用的代理，格式为`<protocal>://<host>:<port>`
	
+   `checkStatus: Bool`（可空）

    是否检查状态码。如果为`true`并且状态码非 2XX，当作失败。默认为`False`。
	
+   `textThreads: Integer`（可空）

    爬取文本的线程数，默认为 5
	
+   `imgThreads: Integer`（可空）

    爬取图片的线程数，默认为 5
	
+   `external: String`（可空）

    外部脚本的路径。脚本中可定义`get_toc`和`get_article`函数来自定义获取目录和正文的逻辑。
	
	`get_toc(html: string, url: string): [string]`
	
	接受页面 HTML 和 URL，返回目录列表
	
	`get_article(html: string, url: string): {'title': string, 'content': string}`
	
	接受页面 HTML 和 URL，返回字典，`title`键是标题，`content`键是正文
	
	⚠该配置项会覆盖`link`，`title`和`content`，但不会覆盖`list`⚠

用于抓取我们的 PyTorch 1.4 文档的示例：

```json
{
    "name": "PyTorch 1.4 中文文档 & 教程",
    "url": "https://gitee.com/apachecn/pytorch-doc-zh/blob/master/docs/1.4/SUMMARY.md",
    "link": ".markdown-body li a",
    "remove": "a.anchor",
    "headers": {"Referer": "https://gitee.com/"}
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
