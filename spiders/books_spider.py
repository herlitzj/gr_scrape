import scrapy
from goodreads.items import BooksItem

class BookSpider(scrapy.Spider):
    name = "books"
    book_list = [1141446]
    allowed_domains = ["goodreads.com"]

    for book in book_list:
        start_urls = ["https://www.goodreads.com/book/show/{0}".format(book)]

        def parse(self, response):
            item = BooksItem()
            item["isbn10"] = response.xpath('//div[@id="bookDataBox"]/div/div/text()').re('[0-9]{10}')[0]
            item["isbn13"] = response.xpath('//div[@id="bookDataBox"]/div/div/span/span/text()').re('[0-9]{13}')[0]
            item["book_id"] = response.xpath('//img[@id="coverImage"]').re('/([0-9]+)')[1]
            item["title"] = response.xpath("//h1[@id='bookTitle']/text()").extract() 
            item["publisher"] = response.xpath('//div[@id="details"]/div[2]/text()').re('[a-z]{2} ([a-zA-Z ]+)')
            item["pub_year"] = response.xpath('//div[@id="details"]/div[2]/text()').re('([0-9]{4})')
            item["description"] = response.xpath('//div[@id="metacol"]').xpath('//div[@id="description"]/span/text()').extract()
            item["img_url"] = response.css('img#coverImage::attr("src")').extract()
            item["genre_list"] = ",".join(set(response.xpath('//div[@class="left"]/a[@class="actionLinkLite"]/text()').extract()))
            item["authors"] = ",".join(set(response.xpath('//span[@itemprop="name"]/text()').extract()))
            yield item
