#!usr/bin/python
#DNS Brute Forcer, uses wordlist to find subdomains.
#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import threading, time, random, sys, socket
from copy import copy

if len(sys.argv) !=3:
	print "Usage: ./dnsbrute.py <server> <wordlist>"
	sys.exit(1)

try:
  	words = open(sys.argv[2], "r").readlines()
except(IOError): 
  	print "Error: Check your wordlist path\n"
  	sys.exit(1)

print "\n\t   d3hydr8[at]gmail[dot]com dnsBruteForcer v1.0"
print "\t--------------------------------------------------\n"
print "[+] Server:",sys.argv[1]
print "[+] Words Loaded:",len(words),"\n"

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
		print "Reloading Wordlist\n"
		reloader()
		value = random.sample(words,  1)
		
	lock.release()
	return value[0]
		
class Worker(threading.Thread):
	
	def run(self):
		value = getword()
		try:
			print "-"*12
			digger = value[:-1]+"."+sys.argv[1]
			print "Trying:", digger
			result = socket.getaddrinfo(digger, None, 0, socket.SOCK_STREAM)
			print "\n\t\tWorked:",[x[4][0] for x in result][0]," Hostname:",digger
		except(socket.gaierror), msg: 
			pass
 
for i in range(len(words)):
	work = Worker()
	work.start()
	time.sleep(1)
