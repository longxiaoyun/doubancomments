#coding=utf-8

import random
from scrapy.conf import settings


class RotateUserAgentMiddleware(object):
	"""docstring for RotateUserAgentMiddleware"""
	def __init__(self, agents):
		
		self.agents = agents

	@classmethod
	def from_crawler(cls,crawler):
		return cls(crawler.settings.getlist('USER_AGENTS'))
	def process_request(self,request,spider):
		request.headers.setdefault('User-Agent',random.choice(self.agents))




# class ProxyMiddleware(object):
# 	"""docstring for ProxyMiddleware"""
# 	def process_request(self,request,spider):
		
# 		request.meta['proxy'] = settings.get('HTTP_PROXY')

		
		




		
