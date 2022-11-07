# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# from scrapy.pipelines.images import ImagesPipeline

import os
import shutil

import requests

from .settings import IMAGE_STORE


class OnTheDrawPipeline:
    def download_image(self, url, location, filename):
        file_path = os.path.join(location, f"{filename}.jpg")
        print(f"downloading {file_path}")
        if not os.path.isfile(file_path):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
                }
                r = requests.get(url, headers=headers, stream=True)
                if r.status_code == 200:
                    r.raw.decode_content = True
                    with open(file_path, "wb") as f:
                        shutil.copyfileobj(r.raw, f)
                    print("Image sucessfully Downloaded: ", file_path)
            except Exception as e:
                print("Failed: ", e)

    def process_item(self, item, spider):
        url = item["image_urls"][0]
        location = IMAGE_STORE
        filename = item["file_name"]
        self.download_image(url, location, filename)
        return item
