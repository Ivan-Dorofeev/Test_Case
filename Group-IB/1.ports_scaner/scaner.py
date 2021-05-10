import requests
from bs4 import BeautifulSoup

surl = "http://192.168.1.4"


def get_html(url):
    req = requests.get(url)
    print('req', req)
    if req.status_code == 200:
        return req.content
    else:
        raise Exception("Bad request")


def search(s):
    pass


def lookup_cve(name):
    pass


print(get_html(surl))
print(get_html(surl))
