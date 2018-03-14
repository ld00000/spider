# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import html2text
import os
from os.path import dirname
import errno
import requests
from confluence.items import *

class ConfluencePipeline(object):
    def process_item(self, item, spider):
      if not isinstance(item, ConfluenceItem):
        return item

      fullpath = os.path.join(dirname(os.path.abspath(os.path.dirname(__file__))), "data", item['path'], item['name'] + '.md')

      if not os.path.exists(os.path.dirname(fullpath)):
        try:
          os.makedirs(os.path.dirname(fullpath))
        except OSError as exc: 
          if exc.errno != errno.EEXIST:
            raise

      content = html2text.html2text(item['content'])
      with codecs.open(fullpath, 'w', encoding='utf-8') as f:
        f.write(content)

      return item

class ImgPipeline(object):
  def process_item(self, item, spider):
    if not isinstance(item, ImgItem):
        return item

    imgpath = os.path.join(dirname(os.path.abspath(os.path.dirname(__file__))), "data", item['path'], item['name'])
    with open(imgpath, 'w') as f:
      f.write(item['content'])

    return item