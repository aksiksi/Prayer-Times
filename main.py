# Sources:

# http://docs.python.org/library/time.html
# https://code.google.com/p/python-twitter/
# http://stackoverflow.com/a/4389549
# http://www.saltycrane.com/blog/2007/09/how-to-sort-python-dictionary-by-keys/
# http://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python

import twitter
import time
import urllib2
import time
from BeautifulSoup import BeautifulSoup
from datetime import datetime

api = twitter.Api(consumer_key='koBWbHjp2HIwN7Vc35bQBg', consumer_secret='05shhFc7tLPtM6W6EDNihanLjChCNxwd9Wii0HYMOjk', 
                  access_token_key='558862365-jrYI1A91zsZLA1Z2T4JI6z6557Ig2BETpObo8k6B', 
                  access_token_secret='DApa4dZ4sLDQMiC8RVu07PVP6O0BZgo7H9erki17Pk')

def extract():
    ''' Extracts prayer times for Abu Dhabi from http://awqaf.ae/ and parses them accordingly.'''
    response = urllib2.urlopen("http://awqaf.ae/?Lang=EN")
    source = response.read()

    soup = BeautifulSoup(source)

    div = soup.find("div", "wrap-4 alignLeft push-left-2").findAll("li")

    salah = {}

    for li in div:
        salah[li.span.text] = li.text.replace(li.span.text, '')

    for key, value in salah.iteritems():
        salah[key] = time.strftime('%H:%M', time.strptime(value, '%I:%M %p')) # Lovely time parsing using the built-in time module

    return salah

def main():
    salah = extract()
    count = 0
    sleep = 0 # Set this to a default value

    print "Currently running. Please do not close this window.\n"

    while True:
        now = time.asctime(time.localtime())[11:16]

        if now == '00:10':
            salah = extract()

        for key, value in sorted(salah.iteritems(), key=lambda (key, value): (value, key)):
            if count == 1:
                sleep = datetime.strptime(value, '%H:%M') - sleep
                time.sleep(sleep.seconds - 150)
                sleep, count = 0, 0
            if now == value:
                api.PostUpdate("It's now time for {0} prayer ({1} in Al Ain).".format(key, value))
                print "Tweeted {0} prayer and time.".format(key)
                salah[key] = 'z'
                sleep = datetime.strptime(value, '%H:%M')
                count += 1

if __name__ == '__main__':
    main()