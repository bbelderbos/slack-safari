import sys
from safaribot import del_from_cache, clear_cache

# if called with arg delete bookid, else clear whole cache
if len(sys.argv) > 1:
    print('deleting bookid {} from cache'.format(bookid))
    bookid = sys.argv[1]
    del_from_cache(bookid)
else:
    print('no arg, clearing whole cache')
    clear_cache()
