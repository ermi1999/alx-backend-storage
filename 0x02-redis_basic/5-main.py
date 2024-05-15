#!/usr/bin/env python3
get_page = __import__('web').get_page

res = get_page('http://slowwly.robertomurray.co.uk')
print(res)