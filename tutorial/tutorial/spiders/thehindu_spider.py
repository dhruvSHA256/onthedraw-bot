from typing import Generator, List

import scrapy


class OnTheDraw(scrapy.Spider):
    name: str = "onthedraw"
    start_urls: List[str] = ["https://www.thehindu.com/opinion/cartoon/"]

    def parse(self, response) -> Generator:
        cartoon_links: List = response.css("a.s1-cartoon50-1-img::attr(href)").getall()
        # for cartoon_link in cartoon_links:
        #     yield {"url": cartoon_link}
        yield from response.follow_all(cartoon_links, self.parse_cartoonlink)

    def parse_cartoonlink(self, response) -> Generator:
        img_link: str = response.css(
            ".img-container > picture:nth-child(1) > source:nth-child(1)::attr(srcset)"
        ).get()
        yield {"img_link": img_link}
