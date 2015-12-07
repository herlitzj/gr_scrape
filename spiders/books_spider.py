import scrapy
from goodreads.items import BooksItem
import MySQLdb as mdb

connection = mdb.connect('localhost', 'root', 'root', 'bookRatings');
cursor = connection.cursor()
cursor.execute("SELECT distinct(book_id) FROM ratings")
book_list = list(cursor.fetchall())
url_list = []
for book in book_list:
    url_list.append("https://www.goodreads.com/book/show/{0}".format(book[0]))
print url_list
class BookSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["goodreads.com"]
    start_urls = url_list

    def parse(self, response):
        item = BooksItem()
        item["isbn10"] = response.xpath('//div[@id="bookDataBox"]/div/div/text()').re('[0-9]{10}')[0]
        item["isbn13"] = response.xpath('//div[@id="bookDataBox"]/div/div/span/span/text()').re('[0-9]{13}')[0]
        item["book_id"] = response.xpath('//img[@id="coverImage"]').re('/([0-9]+)')[1]
        item["title"] = response.xpath("//h1[@id='bookTitle']/text()").re("([^\n]+)")[0].strip() 
        item["publisher"] = response.xpath('//div[@id="details"]/div[2]/text()').re('[by]{2} ([\S ]+)')
        item["pub_year"] = response.xpath('//div[@id="details"]/div[2]/text()').re('([0-9]{4})')
        item["language"] = ""
        description = "".join(response.xpath('//div[@id="description"]/span//text()').re("([\S ]+)"))
        item["description"] = description.encode('utf-8')
        item["img_url"] = response.css('img#coverImage::attr("src")').extract()
        item["genre_list"] = ",".join(set(response.xpath('//div[@class="left"]/a[@class="actionLinkLite"]/text()').extract()))
        item["authors"] = ",".join(set(response.xpath('//span[@itemprop="name"]/text()').extract()))
        yield item

