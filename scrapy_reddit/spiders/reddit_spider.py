```python
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy_reddit.items import RedditItem

class RedditSpider(scrapy.Spider):
    name = 'reddit_spider'
    allowed_domains = ['www.reddit.com']
    start_urls = ['http://www.reddit.com']

    def parse(self, response):
        sel = Selector(response)
        posts = sel.xpath('//div[@data-test-id="post-container"]')
        
        for post in posts:
            item = RedditItem()
            item['title'] = post.xpath('.//h3/text()').extract_first()
            item['url'] = post.xpath('.//a/@href').extract_first()
            item['upvotes'] = post.xpath('.//div[@data-test-id="upvote"]/text()').extract_first()
            yield item

        next_page = response.css('a.next-button::attr(href)').extract_first()
        if next_page is not None:
            yield Request(next_page, callback=self.parse)
```