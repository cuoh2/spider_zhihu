# -*- coding: utf-8 -*-
import json
import time

import scrapy
from scrapy import Request

from zhihu.items import ZhihuQuestionItem, ZhihuAnswerItem


class ZhihuspiderSpider(scrapy.Spider):
    name = 'zhihuspider'
    allowed_domains = ['zhihu.com']

    base_url = 'https://www.zhihu.com/api/v4/members/ll_ven/following-questions?include=data%5B*%5D.created%2Canswer_count%2Cfollower_count%2Cauthor&offset={}&limit=20'

    anwser_url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=5&platform=desktop&sort_by=default'


    def start_requests(self):
        for i in range(1,4):
            url = self.base_url.format(i*20)
            yield Request(url=url,callback=self.get_question_url)

    def get_question_url(self,response):
        result = json.loads(response.text)
        data = result.get('data')
        for item in data:
            question_id = item.get('id')

            question = ZhihuQuestionItem()
            question['id'] = question_id
            question['title'] = item.get('title')
            question['answer_count'] = item.get('answer_count')
            question['follower_count'] = item.get('follower_count')
            yield question
            yield Request(url=self.anwser_url.format(question_id),callback=self.parse)



    def parse(self, response):
            result =json.loads(response.text)
            is_end = result.get('paging').get('is_end')
            next_url = result.get('paging').get('next')
            answers = result.get('data')
            for answer in answers:
                answer_item = ZhihuAnswerItem()
                answer_item['id'] = answer.get('id')
                answer_item['question'] = answer.get('question').get('title')
                headline = answer.get('author').get('headline')
                headline = '(' +headline+')' if len(headline) > 0 else ''
                answer_item['author'] = answer.get('author').get('name') + headline
                answer_item['answer'] = answer.get('content')
                answer_item['voteup_count'] = answer.get('voteup_count')
                timestamp = answer.get('updated_time')
                answer_item['create_at'] = time.strftime('%Y-%m-%d',time.localtime(timestamp))
                yield answer_item

            if is_end == False:
                yield Request(next_url,callback=self.parse)