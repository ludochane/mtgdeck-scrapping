import scrapy
from mtgdeck_scrapping.items import DeckItem
from mtgdeck_scrapping.items import CardItem

class DeckSpider(scrapy.Spider):
    name = "deck"
    allowed_domains = ["starcitygames.com"]
    start_urls = [
        "http://sales.starcitygames.com/deckdatabase/deckshow.php?t%5BT1%5D=1&event_ID=&feedin=&start_date=04%2F10%2F2016&end_date=07%2F03%2F2016&city=&state=&country=&start=&finish=&exp=&p_first=&p_last=&simple_card_name%5B1%5D=&simple_card_name%5B2%5D=&simple_card_name%5B3%5D=&simple_card_name%5B4%5D=&simple_card_name%5B5%5D=&w_perc=0&g_perc=0&r_perc=0&b_perc=0&u_perc=0&a_perc=0&comparison%5B1%5D=%3E%3D&card_qty%5B1%5D=1&card_name%5B1%5D=&comparison%5B2%5D=%3E%3D&card_qty%5B2%5D=1&card_name%5B2%5D=&comparison%5B3%5D=%3E%3D&card_qty%5B3%5D=1&card_name%5B3%5D=&comparison%5B4%5D=%3E%3D&card_qty%5B4%5D=1&card_name%5B4%5D=&comparison%5B5%5D=%3E%3D&card_qty%5B5%5D=1&card_name%5B5%5D=&sb_comparison%5B1%5D=%3E%3D&sb_card_qty%5B1%5D=1&sb_card_name%5B1%5D=&sb_comparison%5B2%5D=%3E%3D&sb_card_qty%5B2%5D=1&sb_card_name%5B2%5D=&card_not%5B1%5D=&card_not%5B2%5D=&card_not%5B3%5D=&card_not%5B4%5D=&card_not%5B5%5D=&order_1=finish&order_2=&limit=25&action=Show+Decks&p=1"
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
            deck['cards'] = []
            deck_absolute_url = response.urljoin(deck['url'])
            yield scrapy.Request(deck_absolute_url, callback=self.parse_deck, meta={'deck': deck})

    def parse_deck(self, response):
        deck = response.meta['deck']

        for card_wrapper in response.xpath('//div[@class="deck_card_wrapper"]//li'):
            card = CardItem()
            card['occurrence'] = card_wrapper.xpath('text()')
            card['name'] = card_wrapper.xpath('/a/text()')
            deck['cards'].append(card)

        print deck
