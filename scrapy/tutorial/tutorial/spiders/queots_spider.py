import scrapy
class QuotesSpider(scrapy.Spider):
    name="quotes"
    start_urls=[
        'http://quotes.toscrape.com/page/1/'
    ]

    def parse(self,response):

        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'page':response.url,
                'text':quote.xpath('./span/text()').get(),
                'author':quote.xpath('./span/small/text()').get(),
                'tags':quote.xpath('./div[@class="tags"]//a/text()').getall(),
            }
        next_page=response.xpath('//nav/ul/li/a/@href').get()
        if next_page is not None:
            next_page=response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse)