import sys
import os
import sqlite3
import hashlib
import time
import threading

# Hashing
def hashcrypt(type, text):
	text = text.encode()
	if type == "sha1":
		return hashlib.new("sha1", text).hexdigest()
	elif type == "md5":
		return hashlib.md5(text).hexdigest()

# Color Code
class color:
	if os.name == "nt":
		r = ""
		g = ""
		y = ""
		b = ""
		p = ""
		w = ""
		n = ""
	else:
		r = "\033[91m"
		g = "\033[92m"
		y = "\033[93m"
		b = "\033[94m"
		p = "\033[95m"
		w = "\033[97m"
		n = "\033[0m"

# Show Text or Print Text
def show(text, flush=False, other=""):
	waktu = (time.ctime(time.time()).split(" "))[4]
	showText = ("%s[%s%s%s] %s" % (color.w, color.b, waktu, color.w, text))
	if flush == True:
		print ("\r"+showText, end="", flush=True)
	else:
		print (other+showText)

def banner():
	logo = """
%s     .-""-.
    / .--. \\
   / /    \ \   %s ╦ ╦┌─┐┌─┐┬ ┬╦╔╦╗%s
   | |    | |   %s ╠═╣├─┤└─┐├─┤║ ║║%s
   | |.-""-.|    %s╩ ╩┴ ┴└─┘┴ ┴╩═╩╝%s
  ///`.::::.`\  %sAuthor %s:%s Billal%s
 ||| ::/  \:: ; %sVersion%s:%s BETA [0.1]%s
 ||; ::\__/:: ; %sTeams %s :%s Cyber Ghost ID%s
  \\\\\ '::::' /         :%s Black Coder Crush%s
    `=':-..-'`%s
""" % (color.r, color.g, color.r, color.g, color.r, color.g, color.r, color.b, color.r, color.y, color.r, color.b, color.r, color.y, color.r, color.b, color.r, color.y, color.r, color.y, color.r, color.n)
	print(logo)

class hash:
	def __init__(self, hash):
		self.hash = hash
		self.data = []
		self.db = ["/sdcard/hash.db"]
		self.found = 0
		self.type = None

	def checkHash(self):
		if len(self.hash) == 32:
			self.type = "md5"
		elif len(self.hash) == 40:
			self.type = "sha1"
		else:
			show("%s[%sERROR%s]: %sUnknown Hash" % (color.w, color.r, color.w, color.r))
			sys.exit()

	def readDB(self):
		show("%s[%sWARNING%s]: %sReading databases" % (color.w, color.y, color.w, color.y))
		for a in self.db:
			try:
				con = sqlite3.connect(a)
				cur = con.cursor()
				cur.execute("SELECT * FROM wordlist")
				for text in cur:
					self.data.append(text[1])
			except:
				show("%s[%sERROR%s]: %sDatabases error" % (color.w, color.r, color.w, color.r))
				sys.exit()
		show("%s[%sWARNING%s]: %sSucces read databases" % (color.w, color.y, color.w, color.g))

	def md5(self):
		show("%s[%sINFO%s]: %sStarting" % (color.w, color.g, color.w, color.y))
		show("%s[%sINFO%s]: %sType %sMD5" % (color.w, color.g, color.w, color.y, color.b))
		th = threading.Thread(target=self.readDB)
		th.start()
		th.join()
		id = 0
		jml = len(self.data)
		for a in self.data:
			id += 1
			crypt = hashcrypt("md5", a)
			if crypt == self.hash:
				show("%s[%sFOUND%s]: %sHash: %s, result: %s" % (color.w, color.g, color.w, color.g, self.hash, a), other="\n")
				self.found += 1
				sys.exit()
			show("%s[%sCRACKING%s]: %s/%s" % (color.w, color.y, color.w, id, jml), flush=True)
		if self.found == 0:
			show("%s[%sERROR%s]: %sFailed to crack hash" % (color.w, color.r, color.w, color.r), other="\n")

	def sha1(self):
                show("%s[%sINFO%s]: %sStarting" % (color.w, color.g, color.w, color.y))
                show("%s[%sINFO%s]: %sType %sSHA1" % (color.w, color.g, color.w, color.y, color.b))
                th = threading.Thread(target=self.readDB)
                th.start()
                th.join()
                id = 0
                jml = len(self.data)
                for a in self.data:
                        id += 1
                        crypt = hashcrypt("sha1", a)
                        if crypt == self.hash:
                                show("%s[%sFOUND%s]: %sHash: %s, result: %s" % (color.w, color.g, color.w, color.g, self.hash, a), other="\n")
                                self.found += 1
                                sys.exit()
                        show("%s[%sCRACKING%s]: %s/%s" % (color.w, color.y, color.w, id, jml), flush=True)
                if self.found == 0:
                        show("%s[%sERROR%s]: %sFailed to crack hash" % (color.w, color.r, color.w, color.r), other="\n")

	def crack(self):
		self.checkHash()
		if self.type == "md5":
			self.md5()
		elif self.type == "sha1":
			self.sha1()
		else:
			print ()
			sys.exit()


if __name__ == "__main__":
	os.system("cls" if os.name == "nt" else "clear")
	banner()
	try:
		hashid = hash(sys.argv[1])
		th = threading.Thread(target=hashid.crack)
		th.start()
	except IndexError:
		show("%s[%sWARNING%s]: %sPlease input hash" % (color.w, color.y, color.w, color.y))
		show("%s[%sINFO%s]: Use: %s./%s <your hash>" % (color.w, color.g, color.w, color.g, sys.argv[0]))
