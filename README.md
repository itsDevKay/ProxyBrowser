PROXYBROWSER:
==============
ProxyBrowser is a simple script that uses Splinter/Selenium to create a web browser using a proxy to listen on 
our localhost for a Tor connection. Once connected, depending on the interval amount you designated, your ip will change
dynamically to give you a rotating identity for that one extra layer of protection.

USE:
=====
  `python3 ProxyBrowser.py -i <amount of seconds before rotating identity>`

if you want to chmod it.
`$ [sudo] chmod +x ProxyBrowser.py`

then run  ->  `$ ./ProxyBrowser.py -i <amount of seconds before rotating identity>`
