# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RatingsItem(scrapy.Item):
    book_id = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    rating = scrapy.Field()
    isbn10 = scrapy.Field()

class BooksItem(scrapy.Item):
    book_id = scrapy.Field()
    isbn10 = scrapy.Field()
    isbn13 = scrapy.Field()
    title = scrapy.Field()
    publisher = scrapy.Field()
    pub_year = scrapy.Field()
    language = scrapy.Field()
    description = scrapy.Field()
    img_url = scrapy.Field()
    genre_list = scrapy.Field()
    authors = scrapy.Field()

class UserItem(scrapy.Item):
    user_id = scrapy.Field()
    location = scrapy.Field()
    zipcode = scrapy.Field()
    gender = scrapy.Field()
