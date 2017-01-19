# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.spiders import Spider
from scrapy.http import Request ,FormRequest
from doubantest.items import DoubantestItem
import scrapy
from scrapy import log
import re

import sys
reload(sys)  
sys.setdefaultencoding('utf-8')

class CommentSpider(Spider):
    name = "comments"

    start_urls=["https://movie.douban.com/subject/25911694/comments?sort=new_score&status=P"]







    def start_requests(self):          
            yield Request("https://accounts.douban.com/login?source=movie", meta={'cookiejar':1},callback=self.post_login)

    def post_login(self,response):
        print 'Preparing login'       
        sel = Selector(response)
        nodes = sel.xpath("//*[@class='captcha_image']/@src").extract()
        if nodes :           
            print nodes
            xerf = raw_input()
            return scrapy.FormRequest.from_response(
                                                    response,
                                                    meta={'cookiejar': response.meta['cookiejar']},
                                                    formdata={
                                                              'captcha-solution': xerf,
                                                              'form_email': 'username',
                                                              'form_password': 'pwd'  
                                                    },
                                                    callback=self.after_login
                                                    )

        return scrapy.FormRequest.from_response(
                response,
                meta={'cookiejar': response.meta['cookiejar']},
                formdata={'form_email': 'username',
                          'form_password': 'pwd'  
                        },
                callback=self.after_login
        )
    def after_login(self,response):
        #check login succeed before going on
        if "authentication failed" in response.body:
            self.log("login failed", level = log.ERROR)
        for url in self.start_urls :
            print url
            req = Request(url, meta={'cookiejar': response.meta['cookiejar']})
            yield req



    def parse(self,response):


        reg=re.compile('\s+')
        sel = Selector(text=response.body)
        Url = response.url
        start_index = Url.find('comments')
        URL = Url[0:start_index+8]
        ID = filter(str.isdigit,URL)
        comment_item=sel.xpath('//*[@class="comment"]')
        for items in comment_item:
            item = DoubantestItem()
            item['ID']=ID
            item['user_name']=items.xpath('h3/span[@class="comment-info"]/a/text()').extract()
            score=items.xpath('h3/span[@class="comment-info"]').xpath('span[2]/@title')
            # print 'score--------->',score.extract()
            item['user_score']=score.extract()
            item['comment_data']=items.xpath('h3/span[@class="comment-info"]/span[@class="comment-time "]/text()').extract()
            item['comment']=items.xpath('p/text()').extract()
            yield item


        for url in sel.xpath("//*[@class='next']/@href").extract():
            yield Request(URL+url,callback=self.parse,meta={'cookiejar': response.meta['cookiejar']})




