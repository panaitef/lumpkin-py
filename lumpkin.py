#!/usr/bin/python
import sys
import subprocess
import os, tempfile
def debug(output):
	if True:
		print output
def setupChunking(file1,file2, chunkSize):
	""" Given two files creates two temporary folders and splits the files into that location """
	
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
	""" Returns and stores  two lists of consecutive and non-consecutive differences """
	filesA=os.listdir(root+"/A/")
	filesB=os.listdir(root+"/B/")
	filesA.sort()
	filesB.sort()
	substract=[]
	currentA=None
	currentAlist=[]
	currentB=None
	currentBlist=[]
	lastPos=0
	altPos=0
	lastPoslist=[]
	listc=[]
	listd=[]
	
	for i in filesB:
		if not i in filesA:
			print "%s appears in %s, but not in %s"%(i, root+"/B",root+"/A")
	for i in filesA:
		if not i in filesB:
			print "%s appears in %s, but not in %s"%(i, root+"/A",root+"/B")
		dl=diffList(root+"/A/"+i,root+"/B/"+i)
		if len(dl)>0: print i,dl
		for i in dl:
			if currentA==None:
				lastPos=i[0]-1
				currentA=i[1]
				currentB=i[2]
			if lastPos==i[0]-1:
				currentA=i[1]
				currentB=i[2]
				lastPos=i[0]
				altPos+=i[0]
				lastPoslist.append(lastPos)
				currentAlist.append(currentA)
				currentBlist.append(currentB)
				lista=[' '.join(map(str, currentAlist))]
				listb=[' '.join(map(str, currentBlist))]
			else:
				lastPos=i[0]
				altPos=i[0]
				currentA=i[1]
				currentB=i[2]
				substract.append((altPos,currentA,currentB))
			
	
	listc.append((lastPoslist,lista,listb))
	with open("ConsecutiveDiffs", 'w') as file:
   		for item in listc:
        		file.write("{}\n".format(item))
	with open("RandomDiffs", 'w') as file:
   		for item in substract:
        		file.write("{}\n".format(item))
	print "ConsecutiveDiffs"
	print listc
	print "/n RandomDiffs"
	print substract

def dumpSnippets(filename, diffs):
	""" Returns a list of strings, extracted from filneame at positions in the list diffs, in theorder given in diffs """
	#open a file: f=open("dfdff","rb")
	#goto loc: f.seek(1234)
	#Get data: d=f.read(4444) #reads 4444 chars
	pass



if __name__=="__main__":
	print " Copyright (C)  2014 Florina-Alina Panaite.\n Permission is granted to copy, distribute and/or modify this document \n under the terms of the GNU Free Documentation License, Version 1.3\n or any later version published by the Free Software Foundation;\n with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.\n A copy of the license is included in the section entitled GNU Free Documentation License."
	print "Lumpkin is starting"
	print sys.argv
	if len(sys.argv) != 4:
		print "Usage of too many options\n lumpkin.py 'file1' 'file2' 'chunksize'"
		sys.exit(1)

	loc= setupChunking(sys.argv[1],sys.argv[2],sys.argv[3])
	#for i in diffList(loc+"/A/aa",loc+"/B/aa"):
	#	print i
	diffChunks(loc)
