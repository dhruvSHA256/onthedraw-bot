from typing import Generator, List

import scrapy

from ..items import OnTheDrawItem


class OnTheDraw(scrapy.Spider):
    name: str = "onthedraw"
    page_no: int = 1
    start_urls: List[str] = ["https://www.thehindu.com/opinion/cartoon"]

    def parsename(self, name):
        return (
            name.get()
            .replace("\n", "")
            .lower()
            .replace(" ", "_")
            .replace(",", "")
            .replace("—", "")
            .replace("__", "_")
        )

    def parse(self, response) -> Generator:
        cartoon_links: List = response.css("a.s1-cartoon50-1-img::attr(href)").getall()
        if cartoon_links:
            yield from response.follow_all(cartoon_links, self.parse_cartoonlink)
        if OnTheDraw.page_no < 15:
            OnTheDraw.page_no += 1
            next_page: str = f"{OnTheDraw.start_urls[0]}/?page={OnTheDraw.page_no}"
            yield response.follow(next_page, callback=self.parse)

    def parse_cartoonlink(self, response) -> Generator:
        item = OnTheDrawItem()
        img_link: str = response.css(
            ".img-container > picture:nth-child(1) > source:nth-child(1)::attr(srcset)"
        ).get()
        name: str = self.parsename(response.css(".title::text"))
        item["file_name"] = name
        item["image_urls"] = [img_link]
        yield item
