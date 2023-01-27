import scrapy


class ScrapySpider(scrapy.Spider):
    name = 'mycrawler'
    allowed_domains = ['nofluffjobs.com']
    start_urls = ['https://nofluffjobs.com/pl/backend?page=2','https://nofluffjobs.com/pl/frontend?page=2', 'https://nofluffjobs.com/pl/fullstack?page=2', 'https://nofluffjobs.com/pl/mobile?page=2']

    def parse(self, response):
       #for offers in response.css('div.list-container.ng-star-inserted a'):
       for n in response.css('nfj-layout.jobs.ng-star-inserted'): 
     
                
            yield {
                'offername' : n.css('div.list-container.ng-star-inserted a h3::text').getall(),
                'offerpay'  : n.css('span.text-truncate.badgy.salary.tw-btn.tw-btn-secondary-outline.tw-btn-xs.ng-star-inserted::text').getall(),#.replace(u'\xa0', u' '),
                'offerlocation' : n.css('span.tw-text-ellipsis.tw-overflow-hidden.tw-whitespace-nowrap.tw-text-right::text').getall(),                
                'language' : n.css('object.text-truncate.ng-star-inserted ::text').getall()                                                                                                                                                                                       
              }

            next_page = response.xpath('/html/body/nfj-root/nfj-layout/nfj-main-content/div/nfj-postings-search/div/common-main-loader/div/nfj-search-results/div/nfj-pagination/ul/li[9]/a').attrib['href']
            if next_page is not None:
                next_page_link = response.urljoin(next_page)
                yield scrapy.Request(url=next_page_link, callback= self.parse)
