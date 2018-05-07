# -*- coding: utf-8 -*-

import re, urlparse
import sys



def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )

import urllib
from bs4 import BeautifulSoup
from urllib2 import urlopen



def img_save(link, i):
    urllib.urlretrieve(link,  str(i) +"."+ str(link[-3:]))
    print str(i) +"."+ str(link[-3:])


def parse_imgs(URL):
    html_doc = urlopen(URL).read()
    soup = BeautifulSoup(html_doc, "lxml")

    tags = soup.findAll('img')
    data = (set(tag['src'] for tag in tags))

    print str(len(data))+" images found..\n" + "Do you want to continue? [Y/n]"
    answ = raw_input("-->")
    if answ == 'Y' or answ == 'y':
    	print "Downloading.. [Ctrl+C for abort]"
        parse_imgs.i = 0
        for item in data:
            img_save(iriToUri(item), parse_imgs.i)
            parse_imgs.i = parse_imgs.i + 1
    else:
    	print "Abort."


def uri_validator(x):
    try:
        result = urlparse.urlparse(x)
        return result.scheme and result.netloc and result.path
    except:
        return False


def main():
	for param in sys.argv:
		try:
			if uri_validator(param):
				parse_imgs(param)
		except KeyboardInterrupt:
			print "\n Abort."


if __name__ == "__main__":
    main()