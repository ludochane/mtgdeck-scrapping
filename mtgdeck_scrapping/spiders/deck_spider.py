import scrapy
from mtgdeck_scrapping.items import DeckItem
from mtgdeck_scrapping.items import CardItem

class DeckSpider(scrapy.Spider):
    name = "deck"
    allowed_domains = ["starcitygames.com"]
    start_urls = [
        "http://sales.starcitygames.com//deckdatabase/deckshow.php?&t%%5BC1%%5D=1&start_date=06/26/2016&end_date=07/03/2016&start_num=%s&limit=10" % start_num for start_num in xrange(0, 21, 10)
    ]

    def parse(self, response):
        for deckTr in response.xpath('//tr[count(td)=7]'):
            deck = DeckItem()
            deck['name'] = deckTr.xpath('td[1]/a/strong/text()').extract()
            deck['url'] = deckTr.xpath('td[1]/a/@href').extract()
            deck['finish'] = deckTr.xpath('td[2]/span/text()').extract()
            deck['player'] = deckTr.xpath('td[3]/text()').extract()
            deck['event'] = deckTr.xpath('td[4]/text()').extract()
            deck['format'] = deckTr.xpath('td[5]/text()').extract()
            deck['date'] = deckTr.xpath('td[6]/a/text()').extract()
            deck['location'] = deckTr.xpath('td[7]/a/text()').extract()
            deck['maincards'] = []
            print deck
            #deck_absolute_url = response.urljoin(deck['url'])
            #yield scrapy.Request(deck_absolute_url, callback=self.parse_deck, meta={'deck': deck})

    def parse_deck(self, response):
        deck = response.meta['deck']

        for card_wrapper in response.xpath('//div[@class="deck_card_wrapper"]//li'):
            card = CardItem()
            card['occurrence'] = card_wrapper.xpath('text()')
            card['name'] = card_wrapper.xpath('/a/text()')
            deck['maincards '].append(card)

        print deck
