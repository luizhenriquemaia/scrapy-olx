import scrapy
from olx.items import OlxItem


class QuotesSpider(scrapy.Spider):
    name = "property"
    allowed_domains = ['go.olx.com.br']

    def __init__(self, region, apartment, **kwargs):
        if region == "":
            self.start_urls = 'https://go.olx.com.br/imoveis'
        else:
            region.replace(" ", "-")
            if apartment == "True":
                self.start_urls = [f'https://go.olx.com.br/grande-goiania-e-anapolis/{region}/imoveis/venda/apartamentos']
            else:
                self.start_urls = [f'https://go.olx.com.br/grande-goiania-e-anapolis/{region}/imoveis/venda/casas']

    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)
    
    def parse(self, response):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        last_page_link = response.css("div.sc-hmzhuo.hMZElg.sc-jTzLTM.iwtnNi > a::attr(href)").extract()[0]
        last_page_number = int(last_page_link.split('?o=')[1])
        for page_number in range(2, last_page_number + 1):
            page_url = self.start_urls[0] + f'?o={page_number}'
            yield scrapy.Request(page_url, headers=headers, callback=self.parse_page)

    def parse_page(self, response):
        items = OlxItem()
        property_list = response.css(".sc-1fcmfeb-2.fvbmlV > a")
        for property_item in property_list:
            content = property_item.css("div > div.fnmrjs-2.jiSLYe > div.fnmrjs-4.jflPgo")
            items['href'] = property_item.css("a::attr(href)").extract()
            items['title'] = content.css("div.fnmrjs-6.iNpuEh>div>h2::attr(title)").extract()
            items['text'] = content.css("div.fnmrjs-6.iNpuEh>div>span::text").extract()
            items['price'] = content.css("div.fnmrjs-7.erUydy > div.fnmrjs-9.gqfQzY > div > div > span::text").extract()
            if len(items['price']) > 1:
                items['price'] = items['price'][0]
            date_hour = content.css("div.fnmrjs-7.erUydy > div.fnmrjs-10.gHqbSa > div > div > span::text").extract()
            items['date'] = date_hour[0]
            items['hour'] = date_hour[1]
            yield items
        # get the href =    (".sc-1fcmfeb-2.fvbmlV > a::attr(href)")[0].extract()
        # get text title =  (".sc-1fcmfeb-2.fvbmlV > a > div > div.fnmrjs-2.jiSLYe > div.fnmrjs-4.jflPgo > div.fnmrjs-6.iNpuEh>div>h2::attr(title)")[0]
        ##ad-list > li:nth-child(2) > a > div > div.fnmrjs-2.jiSLYe > div.fnmrjs-4.jflPgo > div.fnmrjs-6.iNpuEh > div:nth-child(3) > span
        # get span text =   (".sc-1fcmfeb-2.fvbmlV > a > div > div.fnmrjs-2.jiSLYe > div.fnmrjs-4.jflPgo > div.fnmrjs-6.iNpuEh>div>span::text")
        # #ad-list > li:nth-child(2) > a > div > div.fnmrjs-2.jiSLYe > div.fnmrjs-4.jflPgo > div.fnmrjs-7.erUydy > div.fnmrjs-9.gqfQzY > div:nth-child(1) > div > span
        # get price =       (".sc-1fcmfeb-2.fvbmlV > a > div > div.fnmrjs-2.jiSLYe > div.fnmrjs-4.jflPgo > div.fnmrjs-7.erUydy > div.fnmrjs-9.gqfQzY > div > div > span::text")
        ##ad-list > li:nth-child(2) > a > div > div.fnmrjs-2.jiSLYe > div.fnmrjs-4.jflPgo > div.fnmrjs-7.erUydy > div.fnmrjs-10.gHqbSa > div > div > span:nth-child(1)
        # get date_hour =   (".sc-1fcmfeb-2.fvbmlV>a>div > div.fnmrjs-2.jiSLYe > div.fnmrjs-4.jflPgo > div.fnmrjs-7.erUydy > div.fnmrjs-10.gHqbSa > div > div > span::text")   