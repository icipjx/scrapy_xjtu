# -*- coding: utf-8 -*-
import scrapy
import scrapy.exporters

from xajtdx.items import HtmlItem


class XajtSpider(scrapy.Spider):
    name = 'xajt'
    # allowed_domains = ['http://www.dyyy.xjtu.edu.cn/jypt/jkzn/jkkp.htm']
    start_urls = ['http://www.dyyy.xjtu.edu.cn/jypt/jkzn/jkkp.htm']

    def parse(self, response):

        ####提取目录页的文章链接
        text_url_list =  response.css('.ul_list a::attr(href)').extract()
        for text_url in text_url_list:
            #####拼接链接
            url = response.urljoin(text_url)
            yield scrapy.Request(url=url,callback=self.parse_html)
        ####获取每一页的翻页链接
        page_next = response.css('.Next::attr(href)').extract_first()
        page_url = response.urljoin(page_next)
        yield scrapy.Request(url=page_url, callback=self.parse)

######获取每篇文章的内容，标题和图片下载链接
    def parse_html(self,response):
        html_selector = response.css('.list_right_two_article')
        #######获取文章内容
        html = response.css('.list_right_two_article').extract_first()
        #########获取文章标题
        title = response.css('.list_right_two_tit::text').extract_first()
        ##########获取图片下载链接
        image_urls =html_selector.css('img::attr(src)').extract()
        image_urls_ful_lists = []
        for i  in image_urls:
            image_urls_ful = response.urljoin(i)
            image_urls_ful_lists.append(image_urls_ful)
        item = HtmlItem()
        item['title'] = title
        item['html'] = html
        item['image_urls_ful'] = image_urls_ful_lists
        item['image_urls_old'] = image_urls
        yield item








