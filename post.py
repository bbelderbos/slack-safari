import logging
import os
from pprint import pprint as pp
import requests
import shelve
import sys
import time

from slacker import Slacker

from book import Book

API_URL = "https://www.safaribooksonline.com/api/v2/search/?query=*&sort=date_added"
CACHE = "books"
CHANNEL = "#safaribooks-new"
NUM_PAGES = 2
SEND_AS_BOTUSER = True
try: 
    TOKEN = os.environ["SLACK"]
except KeyError: 
    print("Please set the environment variable SLACK")
    sys.exit(1)

slack = Slacker(TOKEN)
logging.basicConfig(filename='bot.log',level=logging.DEBUG)

def get_books():
    resp = None
    results = []
    for page in range(NUM_PAGES):
        resp = requests.get(API_URL + "&page=" + str(page))
        results += resp.json()["results"]  
    return results

def cache(bid, book):
    with shelve.open(CACHE) as db:
        if not bid in db:
            db[bid] = book

def in_cache(bid):
    with shelve.open(CACHE) as db:
        return bid in db

def post_message(title):
    slack.chat.post_message(CHANNEL, title,
        attachments=book.get_msg_details(),
        as_user=SEND_AS_BOTUSER)

if __name__ == "__main__":
    books = get_books()
    for b in books:
        bid = b.pop("archive_id")
        book = Book(bid, **b)

        logging.debug("{} - {}".format(bid, book.title))
        if in_cache(bid):
            logging.debug("- cached, skipping")
            continue
        cache(bid, book)

        logging.debug("- sending to slack channel")
        post_message(book.title)
        time.sleep(2)
