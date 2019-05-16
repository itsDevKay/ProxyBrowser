#!/usr/bin/env python3.7

'''
============
ProxyBrowser
============
This is a program that swaps ip idenities on
a splinter chrome browser for x seconds.
this acts as an extreme proxy that changes
identities repeatedly until program exits.

$ [sudo] chmod +x ProxyBrowser.py #this will make ProxyBrowser.py be of use with out calling "python3" before the name
use: ./ProxyBrowser.py -i <seconds>
'''

from stem import Signal #Signal is used to change our IP address on command
from stem.util import term #this is only just to make colored text
from stem.control import Controller #Controller will activate our Tor remote

from splinter import Browser #activates our webbrowser functionality
from selenium import webdriver #webdriver is where we will use our options for the proxy

import time #we are using time to set a time interval before switching identities
import argparse #we want to add an argument on how many seconds our time interval is going to be


'''
This function starts a controller from stem's port 9151 and
changes signal (or identity)

more info check out
https://stem.torproject.org/tutorials/the_little_relay_that_could.html
'''
def change_ip():
    with Controller.from_port(port = 9151) as controller:
        controller.authenticate() #verifies the controller. Check the link above if you want to set a password here
        '''
        #if you want your proxy to come out of
        #certain countries, insert the country code here
        #without this setting it will exit where it chooses randomly

        controller.set_options({
            'ExitNodes': '{US}, {RU}, {CA}'
        })
        '''
        controller.signal(Signal.NEWNYM) #Signal.NEWNYM instructs stem to change our identity.
        time.sleep(3) #small delay to give it time to swap identities


if __name__ == '__main__':
    parser = argparse.ArgumentParser() #initializes our arguments we want to add
    parser.add_argument('-i', '--interval', type=int, required=True,
            help="time in seconds before changing the IP identity")
    args = parser.parse_args() #compiles the argument together so we can call it later (e.g. args.interval)

    if args.interval: # if exists
        intervals = args.interval
        print(term.format('[+] Setting time interval to %d seconds' % (args.interval), term.Color.GREEN))

    PROXY = '127.0.0.1:9150' #our proxy will funnel through our localhost via port 9150 and connect to Tor
    executable_path = {'executable_path': '/path/to/chromedriver'}
    chrome_options = webdriver.ChromeOptions() #here we go about modifying settings for our splinter browser
    chrome_options.add_argument("--proxy-server=socks5://%s" % PROXY) #sets our browser settings to use a socks5 proxy connecting to Tor via our localhost

    #initializing our browser using google chrome and using our chromedriver as our executable.
    # we are also connecting our custom browser settings to our browser
    browser = Browser('chrome', **executable_path, options=chrome_options)
    browser.visit('https://whatismyip.host') #this is where i usually check my ip, but the browser will start on this page, you can change it if you want.


    '''

    finally we will run an endless loop to change our ip identity
    while we are using our proxy browser
    '''
    while True:
        try: # using a try/except clause to clean of errors
            print(term.format('[-] Initializing new identity', term.Color.YELLOW))
            change_ip() #changing our ip address
            print(term.format('[+] New identity swap successful', term.Color.GREEN))
            time.sleep(intervals) #set to whatever number placed in argument

        except Exception as e:
            #printing error and exiting script
            print(term.format('[!] %s. exiting ProxyBrowser...' % (str(e))))
            browser.quit()
            break

        except KeyboardInterrupt:
            #closing browser in a clean way without the default keyboardinterrupt message
            print(term.format('\n[!] Closing ProxyBrowser and connections. Thanks for using!', term.Attr.BOLD))
            browser.quit()
            break
