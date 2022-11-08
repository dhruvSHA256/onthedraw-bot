import os
import random
import shutil
from time import sleep

from whatsapp_bot.bot import WABot

IMAGE_DIR = "/home/dhruv/r/scrapy-tutorial/images"
DELAY = 60


def get_new_cartoon():
    return random.choice(os.listdir(IMAGE_DIR))


def main():
    bot = WABot()
    bot.start()
    name = "_"
    bot.select_contact(name)
    while True:
        file_to_send = get_new_cartoon()
        file_location = os.path.join(IMAGE_DIR, file_to_send)
        bot.send_attachment(file_location)
        shutil.move(
            os.path.join(IMAGE_DIR, file_to_send),
            os.path.join(f"{IMAGE_DIR}/used", file_to_send),
        )
        sleep(DELAY)


main()
