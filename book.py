import json
import re
from pyisbn import Isbn13

from data import template

AMAZON = "https://www.amazon.com/dp/{}"

class Book: 
    def __init__(self, bid, **kwargs):
        self.bid = bid
        self.b = {}
        for k,v in kwargs.items():
            if type(v) == list:
                v = ", ".join(v)
            self.b[k] = v
        self.b["synopsis"] = self._shorten()
        self.b["amazon"] = self._amazon_url()
        self.title = self.b["title"]
    
    def _shorten(self):
        text = self._strip_html(self.b["description"])
        return text.split(".")[0]

    def _strip_html(self, text):
        return re.sub('<[^<]+?>', '', text)

    def _amazon_url(self):
        isbn10 = str(Isbn13(self.b["isbn"]).convert())
        return AMAZON.format(isbn10)

    def get_msg_details(self):
        attachments = template()
        attachments[0]["title"] = self.b["title"]
        attachments[0]["author_name"] = self.b["authors"]
        attachments[0]["image_url"] = self.b["cover_url"]
        attachments[0]["fields"][0]["value"] = self.b["content_type"]
        attachments[0]["fields"][1]["value"] = self.b["virtual_pages"]
        attachments[1]["text"] = self.b["synopsis"]
        attachments[2]["text"] = self.b["amazon"]
        return json.dumps(attachments)

    def __str__(self):
        return self.bid + " => " + str(self.b)


if __name__ == "__main__":
    bookid = "9781449374471"
    info = {'cover_url': 'https://www.safaribooksonline.com/library/cover/9781449374471/', 'content_type': 'book', 'popularity': 0, 'issued': '2017-01-15T00:00:00Z', 'authors': ['Ian F. Darwin'], 'id': 'https://www.safaribooksonline.com/api/v1/book/9781449374471/', 'description': "<span><span><div><p>This cookbook doesn't just teach you how to build Android apps; it also gives you the recipes you need to build real-world applications. Written by the author of the best-selling <i>Java Cookbook</i>, and with contributions from many members of the Android community, this book shows you how to do everything: working with multitouch, dealing with the phone (and the camera, accelerometer, GPS, and other built-in devices), working with web services, packaging an app for sale in the Android Market, and more.</p><p>This revised second edition includes new recipes on JSON, material design, and Android Studio IDE. If this book doesn't show you how to do it, you probably don't need it. The Android is gradually overtaking the iPhone as the hottest platform in mobile computing. Make sure you're on the bandwagon.</p></div></span></span>", 'content_format': 'book', 'number_of_reviews': 0, 'average_rating': 0, 'url': 'https://www.safaribooksonline.com/api/v1/book/9781449374471/', 'isbn': '9781449374433', 'source': 'application/epub+zip', 'date_added': '2016-11-16T20:26:34.145Z', 'timestamp': '2016-11-16T20:30:08.706Z', 'virtual_pages': 787, 'title': 'Android Cookbook, 2nd Edition', 'language': 'en', 'format': 'book', 'publishers': ["O'Reilly Media, Inc."], 'web_url': 'https://www.safaribooksonline.com/library/view/android-cookbook-2nd/9781449374471/'}
    b = Book(bookid, **info)
    print(b)
    print("\n--\nAttachments:")
    print(b.get_msg_details())
