# Author: Billal Fauzan
# Version: 0.3

import os
import sys
import sqlite3
import time
import hashlib
import glob
import threading
import optparse

# === COLOR ===
class color:
	if os.name == "nt":
		r = ""
		g = ""
		y = ""
		b = ""
		b = ""
		p = ""
		w = ""
		n = ""
	else:
		r = "\033[1;91m" # RED
		g = "\033[1;92m" # GREEN
		y = "\033[1;93m" # YELLOW
		b = "\033[1;94m" # BLUE
		p = "\033[1;95m" # PURPLE
		w = "\033[97;1m" # WHITE
		n = "\033[0m" # NORMAL

def show(text, flush=False, other=""):
	waktu = (time.ctime(time.time()).split(" "))[3]
	result = "%s%s[%s%s%s] %s" % (other, color.w, color.b, waktu, color.w, text)
	if flush == True:
		print("\r"+result, flush=True, end="")
	else:
		print(result)

def banner(help=False, msg=""):
	os.system("cls" if os.name == "nt" else "clear")
	logo = """
%s     .-""-.
    / .--. \\
   / /    \ \   %s ╦ ╦┌─┐┌─┐┬ ┬╦╔╦╗%s
   | |    | |   %s ╠═╣├─┤└─┐├─┤║ ║║%s
   | |.-""-.|    %s╩ ╩┴ ┴└─┘┴ ┴╩═╩╝%s
  ///`.::::.`\  %sAuthor %s:%s Billal%s
 ||| ::/  \:: ; %sVersion%s:%s BETA [0.3]%s
 ||; ::\__/:: ; %sTeams %s :%s Cyber Ghost ID%s
  \\\\\ '::::' /         :%s Black Coder Crush%s
    `=':-..-'`%s
""" % (color.r, color.g, color.r, color.g, color.r, color.g, color.r, color.b, color.r, color.y, color.r, color.b, color.r, color.y, color.r, color.b, color.r, color.y, color.r, color.y, color.r, color.n)
	print(logo)
	if help == True:
		if msg != "":
			show("%s[%sWARNING%s]: %s%s" % (color.w, color.y, color.w, color.y, msg))
		helper = """Options:
  -h = helper
  -f = multi crack
  -t = single crack
  -a = about
  -d = download data
"""
		print (helper)

class hashid:
	def __init__(self, hash="", file=""):
		self.hash = hash
		self.file = file
		self.data = []
		self.found = []

	def crypt(self, type, text):
		hash = hashlib.new(type, text.encode())
		return hash.hexdigest()

	def detectHash(self):
		if len(self.hash) == 32:
			type = "md5"
		elif len(self.hash) == 40:
			type = "sha1"
		elif len(self.hash) == 64:
			type = "sha256"
		elif len(self.hash) == 96:
			type = "sha384"
		elif len(self.hash) == 56:
			type = "sha224"
		elif len(self.hash) == 128:
			type = "sha512"
		else:
			type = color.r+"unknown"
		return type

	def readDB(self):
		show("%s[%sINFO%s]: %sReading Databases" % (color.w, color.g, color.w, color.r))
		scanFile = glob.glob("databases/*.db")
		if len(scanFile) == 0:
			show("%s[%sERROR%s]: %sFile databases not found, please download%s" % (color.w, color.r, color.w, color.r, color.n))
			sys.exit()
		else:
			show("%s[%sWARNING%s]: %sWait a minute, it might take about 10 seconds" % (color.w, color.y, color.w, color.y))
			for file in scanFile:
				try:
					connection = sqlite3.connect(file)
					cursor = connection.cursor()
					cursor.execute("SELECT * FROM wordlist")
					for data in cursor:
						self.data.append(data[1])
				except:
					show("%s[%sERROR%s]: %sFile '%s' not connected" % (color.w, color.r, color.w, color.r, file))
					if len(self.data) == 0:
						sys.exit()
			show("%s[%sINFO%s]: %sSuccess to reading databases" % (color.w, color.g, color.w, color.g))

	def brute(self):
		show("%s[%sINFO%s]: %sStarting Brute Force" % (color.w, color.g, color.w, color.y))
		type = self.detectHash()
		show("%s[%sWARNING%s]: %sType: %s" % (color.w, color.y, color.w, color.y, color.b+type))
		jml = len(self.data)
		id = 0
		for data in self.data:
			id += 1
			try:
				hashing = self.crypt(type, data)
				show("%s[%sCRACKING%s]: %s%s/%s" % (color.w, color.y, color.w, color.p, id, jml), flush=True)
				if hashing == self.hash:
					show("%s[%sFOUND%s]: %sHash: %s, Result: %s" % (color.w, color.g, color.w, color.g, self.hash[:32], data), other="\n")
					self.found.append(data)
					break
			except ValueError:
				show("%s[%sERROR%s]: %sUnknown hash" % (color.w, color.r, color.w, color.r))
				break

	def start(self):
		th = threading.Thread(target=self.brute)
		th.start()

	def multiCrack(self):
		self.readDB()
		o = open(self.file).read()
		for a in o.splitlines():
			self.hash = a
			self.brute()
			print(color.w+"-"*60)


def main():
	parse = optparse.OptionParser(epilog="Hash Brute Force", add_help_option=False)
	parse.add_option("-h", "--h", dest="help", help="Helper", action="store_true")
	parse.add_option("-f", "--file", dest="multi", help="Multi Crack", action="store_true")
	opt, args = parse.parse_args()
	if opt.help:
		banner(help=True)
	elif opt.multi:
		banner()
		try:
			hashID = hashid(file=args[0])
			hashID.multiCrack()
		except IndexError:
			show("%s[%sERROR%s]: %sPlease input file!%s" % (color.w, color.r, color.w, color.r, color.n))
			sys.exit()

if __name__ == "__main__":
	main()
