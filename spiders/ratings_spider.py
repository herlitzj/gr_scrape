import scrapy
from goodreads.items import RatingsItem

class RatingsSpider(scrapy.Spider):
    name = ""
    allowed_domains = ["goodreads.com"]
    start_urls = ["https://www.goodreads.com/book/show/23453112-modern-romance"]

    def parse(self, response):
        item = RatingsItem()
        user_name = response.xpath('//div[@class="left bodycol"]/div/a[@class="user"]/text()').extract()
        item['user_name'] = user_name.encode('utf-8')
        item['rating'] = response.xpath('//div[@class="left bodycol"]/div/a[contains(@class, "static")]/text()').re('([0-5]{1})')[0]
        item['user_id'] = response.xpath('//div[@class="left bodycol"]/div/a[@class="user"]').re('/([0-9]+)')[0]
        item['book_id'] = response.xpath('//img[@id="coverImage"]').re('([0-9]\w+)')[1]
        item['isbn10'] = response.xpath('//div[@id="bookDataBox"]/div/div/text()').re('[0-9]{10}')
        yield item

        for href in response.css("div.bookCarousel > div > ul > li a::attr('href')"):
            url = response.urljoin(href.extract())
            for i in range(1,5):
                nexturl = url + "?page={0}".format(i)
                yield scrapy.Request(nexturl, callback=self.parse)
