import json
import re
from pyisbn import Isbn13

AMAZON = "https://www.amazon.com/dp/{}"
AMAZON_SEARCH = "https://www.amazon.com/gp/search/?field-keywords={}"
QUEUE_LINK = "https://www.safaribooksonline.com/s/queue-on-safari?identifiers={}"

class Book: 
    def __init__(self, bid, **kwargs):
        self.bid = bid
        self.b = {}
        for k,v in kwargs.items():
            if type(v) == list:
                v = ", ".join(v)
            self.b[k] = v
        self.title = self.b["title"]
        self.authors = self.b.get("authors", "")
        self.publishers = self.b["publishers"]
        self.page_count = self.b["virtual_pages"]
        self.cover = self.b["cover_url"]
        self.urls = {
            "safari" : "*<{}|{}>*".format(self.b["web_url"], self.title), 
            "queue" : "<{}|Queue it>".format(self._queue_link()),
            "amazon" : "<{}|Check at Amazon>".format(self._amazon_url()),
        }
    
    def _queue_link(self):
        return QUEUE_LINK.format(self.bid)

    def _strip_html(self, text):
        return re.sub('<[^<]+?>', '', text)

    def _amazon_url(self):
        try:
            isbn10 = str(Isbn13(self.b["isbn"]).convert())
            return AMAZON.format(isbn10)
        except:
            search_str = re.sub(r'[^A-Za-z0-9]', '+', self.title)
            return AMAZON_SEARCH.format(search_str)

    def __str__(self):
        return self.bid + " => " + str(self.b)

    def msg(self):
        fmt_line1 = "{} (by: {} / publisher: {}"
        fmt_line2 = " / page #: {}"
        fmt_line3 = ")\nActions: {} / {}\n"
        msg = fmt_line1.format(self.urls["safari"], 
            self.authors, self.publishers) 
        try:
            if int(self.page_count) > 0:
                msg += fmt_line2.format(self.page_count) 
        except:
            pass
        msg += fmt_line3.format(self.urls["queue"], 
            self.urls["amazon"])
        return msg

if __name__ == "__main__":
    bookid = "9781449374471"
    info = {'cover_url': 'https://www.safaribooksonline.com/library/cover/9781449374471/', 'content_type': 'book', 'popularity': 0, 'issued': '2017-01-15T00:00:00Z', 'authors': ['Ian F. Darwin'], 'id': 'https://www.safaribooksonline.com/api/v1/book/9781449374471/', 'description': "<span><span><div><p>This cookbook doesn't just teach you how to build Android apps; it also gives you the recipes you need to build real-world applications. Written by the author of the best-selling <i>Java Cookbook</i>, and with contributions from many members of the Android community, this book shows you how to do everything: working with multitouch, dealing with the phone (and the camera, accelerometer, GPS, and other built-in devices), working with web services, packaging an app for sale in the Android Market, and more.</p><p>This revised second edition includes new recipes on JSON, material design, and Android Studio IDE. If this book doesn't show you how to do it, you probably don't need it. The Android is gradually overtaking the iPhone as the hottest platform in mobile computing. Make sure you're on the bandwagon.</p></div></span></span>", 'content_format': 'book', 'number_of_reviews': 0, 'average_rating': 0, 'url': 'https://www.safaribooksonline.com/api/v1/book/9781449374471/', 'isbn': '9781449374433', 'source': 'application/epub+zip', 'date_added': '2016-11-16T20:26:34.145Z', 'timestamp': '2016-11-16T20:30:08.706Z', 'virtual_pages': 787, 'title': 'Android Cookbook, 2nd Edition', 'language': 'en', 'format': 'book', 'publishers': ["O'Reilly Media, Inc."], 'web_url': 'https://www.safaribooksonline.com/library/view/android-cookbook-2nd/9781449374471/'}
    b = Book(bookid, **info)
    print(b)
    print(b._amazon_url())
    info.pop("isbn")
    b2 = Book(bookid, **info)
    assert "isbn" not in b2.b
    print(b2._amazon_url())
    print(b2._queue_link())
