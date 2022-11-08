import asyncio
import os
import random
import shutil

from whatsapp_bot.bot import WABot

IMAGE_DIR = "/home/dhruv/r/scrapy-tutorial/images"
DELAY = 10


# TODO
async def fetch():
    print("fetching data")
    await asyncio.sleep(DELAY)


async def send(bot, name):
    def get_new_cartoon():
        return random.choice(os.listdir(IMAGE_DIR))

    try:
        print("sending msg")
        bot.select_contact(name)
        file_to_send = get_new_cartoon()
        file_location = os.path.join(IMAGE_DIR, file_to_send)
        bot.send_attachment(file_location)
        shutil.move(
            os.path.join(IMAGE_DIR, file_to_send),
            os.path.join(f"{IMAGE_DIR}/used", file_to_send),
        )
    except Exception:
        print("An exception occurred")
    finally:
        await asyncio.sleep(DELAY)


async def main():

    bot = WABot()
    bot.start()
    name = "_"
    while True:
        f1 = asyncio.create_task(fetch())
        f2 = asyncio.create_task(send(bot, name))
        await asyncio.wait([f1, f2])


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
