import scrapy
from goodreads.items import RatingsItem

class RatingsSpider(scrapy.Spider):
    name = "ratings"
    allowed_domains = ["goodreads.com"]
    start_urls = ["https://www.goodreads.com/book/show/23453112-modern-romance"]

    def parse(self, response):
        for sel in response.xpath('//div[@id="bookReviews"]//div[@class="left bodycol"]'):
            item = RatingsItem()
            item['user_name'] = sel.xpath('div/a[2]/text()').extract()[0]
            item['rating'] = sel.xpath('div/a[3]/text()').extract()[0][0]
            item['user_id'] = sel.xpath('div/a[2]').re('/([0-9]\w+)')[0]
            item['book_id'] = response.xpath('//img[@id="coverImage"]').re('([0-9]\w+)')[1]
            item['book_isbn'] = response.xpath('//div[@id="bookDataBox"]/div[2]/div[2]/text()').re('[0-9]\w+')[0]
            yield item

        for href in response.css("div.bookCarousel > div > ul > li a::attr('href')"):
            url = response.urljoin(href.extract())
            for i in range(1,5):
                nexturl = url + "?page={0}".format(i)
                yield scrapy.Request(nexturl, callback=self.parse)
