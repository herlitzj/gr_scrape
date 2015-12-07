import scrapy
from goodreads.items import RatingsItem

class RatingsSpider(scrapy.Spider):
    name = "ratings"
    allowed_domains = ["goodreads.com"]
    start_urls = ["https://www.goodreads.com/book/show/23453112-modern-romance"]

    def parse(self, response):
        for sel in response.xpath('//div[@id="bookReviews"]//div[@class="left bodycol"]'):
            item = RatingsItem()
            item['user_name'] = sel.xpath('div/a[@class="user"]/text()').extract()[0]
            item['rating'] = sel.xpath('div/a[contains(@class, "static")]/text()').re('([0-5]{1})')[0]
            item['user_id'] = sel.xpath('div/a[@class="user"]').re('/([0-9]+)')[0]
            item['book_id'] = response.xpath('//img[@id="coverImage"]/@src').re('l/([0-9]+)')
            item['isbn10'] = response.xpath('//div[@id="bookDataBox"]/div/div/text()').re('[0-9]{10}')[0]
            yield item

        for href in response.css("div.bookCarousel > div > ul > li a::attr('href')"):
            url = response.urljoin(href.extract())
            for i in range(1,5):
                nexturl = url + "?page={0}".format(i)
                yield scrapy.Request(nexturl, callback=self.parse)
