from scrapy.spiders import Spider
from scrapy.http.request import Request
from scrapy.selector import Selector
from twitterscraping-mobile.items import TwitterscrapingItem
from w3lib.html import remove_tags
import re

class TwitterSpider(Spider):
	index = 0
	start = '2015-01-01'
	end = '2015-12-31'
	name = "twitter_mobile"
	allowed_domains = ["mobile.twitter.com"]

	start_urls = [
		#"https://mobile.twitter.com/search?f=tweets&vertical=default&q=%22demam%20berdarah%22%20OR%20dbd%20OR%20dhf%20OR%20%22dengue%20fever%22%20OR%20%22dengue%20hemorrhagic%22%20OR%20%22sakit%20db%22%20lang%3Aid%20since%3A"+start+"%20until%3A"+end+"&src=typd"
		"https://mobile.twitter.com/search?f=tweets&vertical=default&q=%22demam%20berdarah%22%20OR%20dbd%20OR%20dhf%20OR%20%22dengue%20fever%22%20OR%20%22dengue%20hemorrhagic%22%20OR%20%22sakit%20db%22%20lang%3Aid"
    ]

	def parse(self, response):
		s = Selector(response)
		next_link = s.xpath('//div[@class="w-button-more"]/a/@href').extract()
		if len(next_link):
			yield Request("https://mobile.twitter.com"+next_link[0], callback=self.parse)
		itemselector = Selector(response).xpath('//*[@id="main_content"]/div/div[3]/table')
		#regex = re.compile(r"([\\]+u\d*)", re.MULTILINE)
		for sel in itemselector:
			self.index += 1
			item = TwitterscrapingItem()
			item['index'] = self.index
			item['username'] = ''.join(
				map(unicode.strip, sel.xpath('tr[1]/td[2]/a/div/text()').extract()))
			tweet = remove_tags(''.join(
				map(unicode.strip, sel.xpath('tr[2]/td/div').extract()))
				).replace('&amp','&').replace('  ','').replace('\n      ','').replace('\n    ','').replace('\n','').replace('\u',' ')
			item['text_tweet'] = u''+tweet
			item['original_tweet'] = ''.join(sel.xpath('tr[2]/td/div/div').extract())
			item['time_tweet'] = ''.join(
				map(unicode.strip, sel.xpath('tr[1]/td[3]/a/text()').extract()))
			item['url'] = ''.join(
				map(unicode.strip, sel.xpath('tr[2]/td/div/@data-id').extract()))
			item['data_id'] = ''.join(
				map(unicode.strip, sel.xpath('tr[3]/td/span[1]/a/@href').extract()))
			yield item