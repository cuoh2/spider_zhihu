# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuQuestionItem(scrapy.Item):

    collection='Question'
    id = scrapy.Field()
    answer_count = scrapy.Field()
    follower_count = scrapy.Field()
    title = scrapy.Field()


class ZhihuAnswerItem(scrapy.Item):
    collection='Answer'

    id = scrapy.Field()
    question = scrapy.Field()
    answer = scrapy.Field()
    voteup_count = scrapy.Field()
    author = scrapy.Field()
    create_at = scrapy.Field()

class DoubanUserItem(scrapy.Item):
    name = scrapy.Field()
    bio = scrapy.Field()
    add = scrapy.Field()
    time = scrapy.Field()