import sys
from safaribot import del_from_cache, clear_cache

# if called with arg delete bookid, else clear whole cache
if len(sys.argv) > 1:
    bookid = sys.argv[1]
    del_from_cache(bookid)
else:
    clear_cache()
