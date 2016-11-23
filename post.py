import logging
import os
import re
import requests
import shelve
import socket
import sys
import time

from slacker import Slacker

from book import Book

ALL_BOOKS_STR = 'safaribooks'
API_URL = "https://www.safaribooksonline.com/api/v2/search/?query=*&sort=date_added&page={}"
BOTLOG = 'bot.log'
CACHE = "books"
NUM_QUERIES = 2
REMOTE = not "MacBook" in socket.gethostname()
SEND_AS_BOTUSER = True
SLEEP = 2
try: 
    TOKEN = os.environ["SLACK"]
except KeyError: 
    print("Please set the environment variable SLACK")
    sys.exit(1)

slack = Slacker(TOKEN)
resp = slack.channels.list()
channels = [chan["name"] for chan in resp.body["channels"] if chan["is_member"]]

logging.basicConfig(level=logging.DEBUG, 
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename=BOTLOG)

def get_books():
    results = []
    for page in range(NUM_QUERIES):
        resp = requests.get(API_URL.format(page))
        results += resp.json()["results"]  
        time.sleep(SLEEP)
    return results

def cache_book(bid, book):
    with shelve.open(CACHE) as db:
        if not bid in db:
            db[bid] = book

def del_from_cache(bid):
    with shelve.open(CACHE) as db:
        if bid in db:
            del db[bid]

def in_cache(bid):
    with shelve.open(CACHE) as db:
        return bid in db

def post_message(title):
    for channel in channels:
        channel = normalize_channel_name(channel)
        if ALL_BOOKS_STR in channel or channel in title:
            slack.chat.post_message('#' + channel, title,
                attachments=book.get_msg_details(),
                as_user=SEND_AS_BOTUSER)

def normalize_channel_name(channel):
    strip_chars = ('-', )
    for s in strip_chars:
        channel = channel.replace(s, ' ')
    return channel

if __name__ == "__main__":
    books = get_books()
    for b in books:
        bid = b.pop("archive_id")
        book = Book(bid, **b)

        logging.debug("{} - {}".format(bid, book.title))
        if in_cache(bid):
            logging.debug("- cached, skipping")
            continue
        cache_book(bid, book)

        if REMOTE:
            logging.debug("- sending to slack channel")
            post_message(book.title)
            time.sleep(SLEEP)
