# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

SEARCH_QUERY = (
    'https://www.imdb.com/search/title?'
    'title_type=feature&'
    'user_rating=1.0,10.0&'
    'countries=us&'
    'languages=en&'
    'count=250&'
    'view=simple'
)


class MovieSpider(CrawlSpider):
    name = 'movie'
    allowed_domains = ['imdb.com']
    start_urls = [SEARCH_QUERY]

    rules = (Rule(
        LinkExtractor(restrict_css=('div.desc a')),
        follow=True,
        callback='parse_query_page',
    ),)

    def parse_query_page(self, response):
        links = response.css('span.lister-item-header a::attr(href)').extract()
        for link in links:
            yield response.follow(link, callback=self.parse_movie_detail_page)

    def parse_movie_detail_page(self, response):
        data = {}
        # print(response.css('.jGRxWM *::text').extract_first())
        # ‘#Selectors *::text’
        data['title'] = response.css('h1::text').extract_first().strip()
        print(response.xpath('/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[6]/div[2]/div[1]/div[1]')[0])
        
        # print(data['title'])
        companies = response.xpath('/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[10]/div[2]/ul/li[7]/div/ul')
        if len(companies) > 0:
            data['production_companies'] = companies[0].xpath('li/a/text()').extract()
        else:
            companies = response.xpath('/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[10]/div[2]/ul/li[6]/div/ul')
            if len(companies) > 0:
                data['production_companies'] = companies[0].xpath('li/a/text()').extract()

        # pc = response.xpath(
        #     '//section[contains(@class, "ipc-page-section")]').getall()[9]
        # for i in pc:
        #     pc.xpath('')
        writers = response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[2]/div/ul')
        data['writers'] = writers[0].xpath('li/a/text()').extract()
        directors =  response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[1]/div/ul')
        data['directors'] = directors[0].xpath('li/a/text()').extract()
        actors = response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[3]/div/ul')
        # for i in actors:
        #     print(i.xpath('li/a/text()').extract())
        data['actors'] = actors[0].xpath('li/a/text()').extract()
        #.gxdDLW
        # data['watch_on'] = response.xpath('//a[contains(@class, "ipc-button")]/@href').extract[1]
        data['watch_on'] = response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div/a/@href').get()
        # data['rating'] = response.css(
        #     '.subtext::text').extract_first().strip() or None
        data['year'] = response.css('.ipc-link *::text').getall()[4]
        data['users_rating'] = response.css('.jGRxWM *::text').extract_first()
        data['votes'] = response.css('.dPVcnq *::text').extract_first()
        # data['metascore'] = response.xpath(
        #     '//div[contains(@class, "metacriticScore")]/span/text()').extract_first()
        data['img_url'] = response.xpath(
            '//div[contains(@class, "ipc-media")]/img/@src').extract_first()
        data['plot'] = response.xpath(
            '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/div[2]/span[3]/text()').extract_first()
        # countries = response.xpath(
        #     '/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[10]/div[2]/ul/li[2]/div/ul/li')
        #     #/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[9]/div[2]/ul/li[2]/div/ul/li
        #     # /html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[9]/div[1]/div/hgroup/h3
        # # print(countries)
        # for c in countries:
        #     print(c.extract())
        #     rows = c.xpath('a/text()').extract()
        #     print(rows)
        # data['countries'] = [country.extract() for country in countries]
        # languages = response.xpath(
        #     '//div[contains(@class, "txt-block") and contains(.//h4, "Language")]/a/text()').extract()
        # data['languages'] = [language.strip() for language in languages]
        # actors = response.xpath('//td[not(@class)]/a/text()').extract()
        # data['actors'] = [actor.strip() for actor in actors]
        # genres = response.xpath(
        #     "//div[contains(.//h4, 'Genres')]/a/text()").extract()
        # data['genre'] = [genre.strip() for genre in genres]
        # tagline = response.xpath(
        #     '//div[contains(string(), "Tagline")]/text()').extract()
        # data['tagline'] = ''.join(tagline).strip() or None
        # data['description'] = response.xpath(
        #     '//div[contains(@data-testid, "plot")]/text()').extract_first().strip() or None
        # directors = response.xpath(
        #     "//div[contains(@class, 'credit_summary_item') and contains(.//h4, 'Director')]/a/text()").extract() or None
        # if directors:
        #     data['directors'] = [director.strip() for director in directors]
        # data['runtime'] = response.xpath(
        #     "//div[contains(@class, 'txt-block') and contains(.//h4, 'Runtime')]/time/text()").extract_first() or None
        data['imdb_url'] = response.url.replace('?ref_=adv_li_tt', '')

        yield data
