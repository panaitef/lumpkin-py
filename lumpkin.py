#!/usr/bin/python
import sys
import subprocess
import os, tempfile
def debug(output):
	if True:
		print output
def setupChunking(file1,file2, chunkSize):
	""" Given two vmdk files, create two temp folders, and chunk the vmdks into them, return the folder names """
	
	debug("Chunking %s and %s into chunks of size %s"%(file1,file2,chunkSize))
	loc=tempfile.mkdtemp(prefix="lumpkin")
	os.mkdir(loc+"/A")
	os.mkdir(loc+"/B")
	os.system("split %s -b %s %s"%(file1,chunkSize,loc+"/A/"))
	os.system("split %s -b %s %s"%(file2,chunkSize,loc+"/B/"))
	debug("Dumping chunks in %s"%loc)
	return loc

def diffList(file1, file2):
	""" Returns a list of differences """
	debug("Diffing %s and %s"%(file1,file2))
	difflist=[]
	a=subprocess.Popen(["cmp", "-l" ,file1, file2], stdout=subprocess.PIPE)
	data=a.communicate()
	for i in data[0].split("\n"):
		if i.strip()!="":
			now=int(i[-3:],8)
			was=int(i[-7:-3],8)
			loc=int(i[:-7])
			difflist.append((loc,was,now))
	return difflist

def diffChunks(root):
	filesA=os.listdir(root+"/A/")
	filesB=os.listdir(root+"/B/")
	filesA.sort()
	filesB.sort()
	global dl
	#Do we quit if we have different image sizes?
	for i in filesB:
		if not i in filesA:
			print "%s appears in %s, but not in %s"%(i, root+"/B",root+"/A")
	for i in filesA:
		if not i in filesB:
			print "%s appears in %s, but not in %s"%(i, root+"/A",root+"/B")
		dl=diffList(root+"/A/"+i,root+"/B/"+i)
		if len(dl)>0: print i,dl

def subtract():
	""" Return a list wit all items from l1 not in l2 """
	global dl
	substract=[]
	currentA=None
	currentB=None
	lastPos=0
	for i in dl:
		if currentA==None or lastPos!=i[0]-1:
			lastPos=i[0]
			currentA=i[1]
			currentB=i[2]
			substract+(currentA,currentB,lastPos)
			
		else:
			currentA+=i[1]
			currentB+=i[2]
			lastPos=i[0]
			substract+(currentA,currentB,lastPos)		
	
	return substract
def dumpSnippets(filename, diffs):
	""" Returns a list of strings, extracted from filneame at positions in the list diffs, in theorder given in diffs """
	#open a file: f=open("dfdff","rb")
	#goto loc: f.seek(1234)
	#Get data: d=f.read(4444) #reads 4444 chars
	pass



if __name__=="__main__":
	print "Lumpkin is starting"
	print sys.argv
	if len(sys.argv) != 4:
		print "Usage...."
		sys.exit(1)

	loc= setupChunking(sys.argv[1],sys.argv[2],sys.argv[3])
	#for i in diffList(loc+"/A/aa",loc+"/B/aa"):
	#	print i
	diffChunks(loc)
	print subtract()