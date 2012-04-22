# Sources:
# http://docs.python.org/library/time.html
# https://code.google.com/p/python-twitter/
# http://stackoverflow.com/a/4389549
# http://www.saltycrane.com/blog/2007/09/how-to-sort-python-dictionary-by-keys/
# http://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python

import twitter
import time
import urllib2
import lxml.etree as etree
from datetime import datetime, timedelta

api = twitter.Api(consumer_key='koBWbHjp2HIwN7Vc35bQBg', consumer_secret='05shhFc7tLPtM6W6EDNihanLjChCNxwd9Wii0HYMOjk',
                  access_token_key='558862365-jrYI1A91zsZLA1Z2T4JI6z6557Ig2BETpObo8k6B',
                  access_token_secret='DApa4dZ4sLDQMiC8RVu07PVP6O0BZgo7H9erki17Pk')

def scrape():
    ''' Scrapes prayer times for Abu Dhabi from http://awqaf.ae/ and parses them accordingly.'''
    page = etree.HTML(urllib2.urlopen("http://awqaf.ae/?Lang=EN").read())

    times = page.xpath("//div[contains(@class, 'wrap-4 alignLeft push-left-2')]//li/text()")[:6]
    prayers_en = page.xpath("//div[contains(@class, 'wrap-4 alignLeft push-left-2')]//li//span/text()")[:6]

    times.pop(1)
    prayers_en.pop(1)

    salah = {}

    for i, j in zip(prayers_en, times):
        salah[i] = j

    for key, value in salah.iteritems():
        t_minus = datetime.strptime(value, '%I:%M %p') - timedelta(minutes=2) # Deduct 2 minutes to convert to Al Ain prayer time
        salah[key] = datetime.strftime(t_minus, '%H:%M') # Lovely time parsing using the built-in datetime module

    return salah

def main():
    salah = scrape()
    count = 0
    sleep = 0 # Set this to a default value

    print "Currently running. Please do not close this window.\n"

    time.sleep(sleep * 3600) # Initial sleep

    while True:
        now = time.asctime(time.localtime())[11:16]

        if now == '00:10':
            salah = scrape()

        for key, value in sorted(salah.iteritems(), key=lambda (key, value): (value, key)):
            if count == 1:
                sleep = datetime.strptime(value, '%H:%M') - sleep
                print "Wake up in {0} hours".format(sleep.seconds / 3600.0)
                time.sleep(sleep.seconds - 120)
                sleep, count = 0, 0
            if now == value:
                api.PostUpdate("It is now time for {0} prayer in Al Ain [{1}].".format(key, value))
                print "Tweeted {0} prayer and time. ({1} at {2})".format(key, time.asctime(time.localtime())[4:10], value)
                sleep = datetime.strptime(value, '%H:%M')
                salah[key] = 'z'
                count += 1

if __name__ == '__main__':
    main()