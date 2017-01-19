# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import re
import MySQLdb

class DoubantestPipeline(object):
	def __init__(self):
		self.file=codecs.open('comments.json','w',encoding='utf-8')
	def process_item(self, item, spider):
		line=json.dumps(dict(item),ensure_ascii=False)+'\n'
		self.file.write(line)
		return item
	def spider_closed(self,spider):
		self.file.closed()


def DBHandler():
	conn=MySQLdb.connect(
		host="",
		user="",
		passwd="",
		charset="utf8",
		db="",
		use_unicode=False
	)
	return conn


class DoubanMySQLPipeline(object):
	"""docstring for DoubanTxtPipeline"""
	def process_item(self,item,spider):
		dbObject=DBHandler()
		cursor=dbObject.cursor()

		sql="INSERT INTO douban_movie (ID,user_name,user_score,comment_data,comment) VALUES (%s,%s,%s,%s,%s)"
		param=(item['ID'],item['user_name'],item['user_score'],item['comment_data'],item['comment'])


		try:
			cursor.execute(sql,param)

			dbObject.commit()

		except Exception, e:
			print e
			dbObject.rollback()

		return item


		
		
