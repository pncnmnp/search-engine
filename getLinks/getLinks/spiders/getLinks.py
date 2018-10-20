import scrapy

class getHarryPotterLinks(scrapy.Spider):
	name="links"
	start_urls=[
		'https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages']

	# This is only suitable for wikipedia links
	# Do change the tags for appropriate scraping
	def parse(self, response):
		for div in response.css('div.mw-content-ltr'):
			for link in div.css('a::attr(href)'):
				if(link.extract()[:6] == '/wiki/'):
					yield {
						'link': response.url[:24]+link.extract()
					}