# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# from scrapy.pipelines.images import ImagesPipeline

import os
import shutil

import psycopg2
import requests

from .settings import IMAGE_STORE


class OnTheDrawPipeline:
    def __init__(self):
        hostname = "localhost"
        username = "postgres"
        password = "postgres1"
        database = "postgres"

        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password, dbname=database
        )

        self.cur = self.connection.cursor()

        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS comics(
            id serial PRIMARY KEY, 
            file_name text,
            image_url text,
            used boolean
        )
        """
        )

    @staticmethod
    def download_image(url, location, filename):
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

        self.cur.execute("select * from comics where file_name = %s", (filename,))
        result = self.cur.fetchone()

        if result:
            spider.logger.warn(f"Item already in database: {filename}")
        else:
            self.download_image(url, location, filename)
            self.cur.execute(
                """ insert into comics (file_name, image_url, used) values (%s,%s,%s)""",
                (filename, url, False),
            )

            self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
