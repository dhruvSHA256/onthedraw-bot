from typing import Generator, List

import scrapy


class QuotesSpider(scrapy.Spider):
    # name of spider used in command ```scrapy crawl quotes```
    name: str = "quotes"
    start_urls: List[str] = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]

    def parse(self, response) -> Generator:
        quotes: List = response.css("div.quote")
        for quote in quotes:
            text: str = quote.css("span.text::text").get()
            author: str = quote.css("small.author::text").get()
            tags: List[str] = quote.css("div.tags a.tag::text").getall()
            yield {
                "text": text,
                "author": author,
                "tags": tags,
            }
