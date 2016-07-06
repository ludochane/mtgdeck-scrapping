import scrapy
from mtgdeck_scrapping.items import DeckItem
from mtgdeck_scrapping.items import CardItem

class DeckSpider(scrapy.Spider):
    name = "deck"
    allowed_domains = ["starcitygames.com"]
    start_urls = [
        #"http://sales.starcitygames.com//deckdatabase/deckshow.php?&t%%5BC1%%5D=1&start_date=01/01/2016&end_date=01/31/2016&start_num=%s&limit=100" % start_num for start_num in xrange(0, 450, 100)
        "http://sales.starcitygames.com//deckdatabase/deckshow.php?&t%%5BC1%%5D=1&start_date=02/01/2016&end_date=06/30/2016&start_num=%s&limit=100" % start_num for start_num in xrange(2400, 5200, 100)
    ]

    def parse(self, response):
        for deckTr in response.xpath('//tr[count(td)=7]'):
            name = deckTr.xpath('td[1]/a/strong/text()').extract()
            if (name):
                deck = DeckItem()
                deck['name'] = name[0]
                deck['url'] = deckTr.xpath('td[1]/a/@href').extract()[0]
                deck['finish'] = deckTr.xpath('td[2]/span/text()').extract()[0]
                deck['player'] = deckTr.xpath('td[3]/text()').extract()[0]
                deck['event'] = deckTr.xpath('td[4]/text()').extract()[0]
                deck['format'] = deckTr.xpath('td[5]/text()').extract()[0]
                deck['date'] = deckTr.xpath('td[6]/a/text()').extract()[0]
                locations = deckTr.xpath('td[7]/a/text()').extract()
                if (locations):
                    deck['location'] = locations[0]
                deck['maincards'] = []
                #yield deck
                yield scrapy.Request(deck['url'], callback=self.parse_deck, meta={'deck': deck})

    def parse_deck(self, response):
        deck = response.meta['deck']

        for card_wrapper in response.xpath('//div[@class="deck_card_wrapper"]//li'):
            card = CardItem()
            card['occurrence'] = card_wrapper.xpath('text()').extract()[0].strip()
            card['name'] = card_wrapper.xpath('a/text()').extract()[0]
            deck['maincards'].append(card)

        yield deck
