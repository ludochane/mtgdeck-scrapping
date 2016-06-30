import scrapy
from mtgdeck_scrapping.items import CardItem

class CardSpider(scrapy.Spider):
    name = "card"
    allowed_domains = ["starcitygames.com"]
    start_urls = [
        "http://sales.starcitygames.com//deckdatabase/displaydeck.php?DeckID=101452"
    ]

    def parse(self, response):
        for card_wrapper in response.xpath('//div[@class="deck_card_wrapper"]//li'):
            card = CardItem()
            card['occurrence'] = card_wrapper.xpath('text()').extract()
            card['name'] = card_wrapper.xpath('a/text()').extract()
            print card
