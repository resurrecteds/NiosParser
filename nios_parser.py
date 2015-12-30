import urllib2
import os.path
import pprint
import time
import sys
import pickle as pickle

"""index is 1, 101 or 201"""
def findFirstLine(linesList, index):
	for i in range(len(linesList)):
		line = linesList[i].strip()
		if line == 	"<td>%s</td>" % (index):
			return i
	return None

""" index is the index of the first record in the table """
def findStepSize(linesList, index, firstLineIndex):
	step = 0;
	assert(index == 1 or index == 101 or index == 201)
	for i in xrange(firstLineIndex, len(linesList), 1):
		line = linesList[i].strip()
		if line == "<td>%s</td>" % (index + 1):
			return step
		step = step + 1
	return None



def createDataFile(filename, url):
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
	response = urllib2.urlopen(req)
	source = response.read();
	with open(filename, 'w') as sourceFile:
		sourceFile.write(source)

	# sourceFile = open(filename, 'w');
	# sourceFile.write(source)
	# sourceFile.close()


def getLinesListFromSourceFile(filename):
	with open(filename, "r") as file:
		linesList = file.readlines()

	return linesList


def getDatabaseFromFile(filename):
	database = []
	for i in range(3):
		with open(filename, 'rb') as file:
			database.append(pickle.load(file))
	return database
	# with open(filename, 'r') as file:
	# 	database = file.readlines();
	# return database;


def makeDatabase(linesList, recordNum):
	localDB = []

	firstLineIndex = findFirstLine(linesList, recordNum)
	assert (firstLineIndex != None)
	step = findStepSize(linesList, recordNum, firstLineIndex)

	j = 0
	for i in range(firstLineIndex, len(linesList), step):
		if j == 100:
			break;

		string = linesList[i].strip()

		data = {}
		data['rank'] = recordNum + j

		fullLine = linesList[i + 10].strip()
		start = fullLine.find('target="_blank">') + 16
		end = fullLine.find("</a>")
		data['player1'] = fullLine[start:end]

		fullLine = linesList[i + 14].strip()
		start = fullLine.find('target="_blank">') + 16
		end = fullLine.find("</a>")
		data['player2'] = fullLine[start:end]

		fullLine = linesList[i + 20].strip()
		start = fullLine.find('class="wins">') + 13
		end = fullLine.find("</td>")
		data['wins'] = fullLine[start:end]

		fullLine = linesList[i + 20].strip()
		start = fullLine.find('class="wins">') + 13
		end = fullLine.find("</td>")
		data['wins'] = fullLine[start:end]

		fullLine = linesList[i + 21].strip()
		start = fullLine.find('class="loses">') + 14
		end = fullLine.find("</td>")
		data['loses'] = fullLine[start:end]


		fullLine = linesList[i + 22].strip()
		start = fullLine.find('class="score">') + 14
		end = fullLine.find("</td>")
		data['score'] = fullLine[start:end]

		fullLine = linesList[i + 23].strip()
		start = fullLine.find('class="rate">') + 13
		end = fullLine.find("</td>")
		data['rate'] = fullLine[start:end]

		localDB.append(data)
		j = j + 1

	return localDB

# todo: delete
def saveTest():
	mylist = [1,2,3,4,5,6,7,8,9]
	with open('test.txt', 'wb') as file:
		pickle.dump(mylist, file)

	mylist = []
	print mylist
	with open('test.txt', 'rb') as file:
		mylist = pickle.load(file)
	print mylist

	dict = {"a":"fddf", "b":"43434"}


def main(argv):
	urls = ["http://nios.kr/sc2/eu/2v2/hots/", "http://nios.kr/sc2/eu/2v2/hots/2", "http://nios.kr/sc2/eu/2v2/hots/3"]
	entries = [1, 101, 201]

	sourceFile = "source.txt"
	outputFile = "database.pckl"

	# TODO: CHANGE
	refreshFile = True
	if not os.path.isfile(sourceFile) or not os.path.isfile(outputFile):
		refreshFile = True;
	else:
		creationTime = os.path.getmtime(sourceFile)
		if int(time.time()) - creationTime > 86400:
			refreshFile = True
	
	if not refreshFile:
		database = getDatabaseFromFile(outputFile)
		
	else:
		file = open("out.txt", 'w')
		database = []
		for i in range(len(urls)):	
			createDataFile(sourceFile, urls[i])
			linesList =  getLinesListFromSourceFile(sourceFile)
			smallerDB = makeDatabase(linesList, entries[i])
			for data in smallerDB:
				file.write("%s\n" % data)

			database.append(smallerDB)

		file.close()

		pickleFile = open(outputFile, 'wb')
		pickle.dump(database, pickleFile)
		pickleFile.close()

	lookupName = argv[0]

	# flag = True;
	print len(database)
	for smallerDb in database:
		# print len(smallerDb)
		for line in smallerDb:
			if lookupName in (line["player1"], line["player2"]):
				print line
	# for i in range(len(urls)):
	# 	# with open(outputFile, 'rb') as file:
	# 	# 	database = pickle.load(file)
	# 		# print database[1]
	# 	print len(database)
	# 	for smallerDb in database:
	# 		if smallerDb == database:
	# 			print "yes"
	# 		print len(smallerDb)
	# 		print smallerDb
	# 		for line in smallerDb:
	# 			if lookupName in (line["player1"], line["player2"]):
	# 				print line
	# 			# todo - uncomment
	# 			# return
	# print "No record found"

	# if len(argv) == 1:
	# 	lookupName = argv[0]
	# 	print "database size is:"

	# 	with open("out.txt", 'r') as databaseFile:
	# 		database = databaseFile.readlines()
	# 	print len(database)

	# 	flag = True;
	# 	for line in database:
	# 		if flag:
	# 			print line[1:13]
	# 			flag = False
	# 		if line == database[1]:
	# 			print "fdsfdfd"

	# 		if lookupName in (line["player1"], line["player2"]):
	# 			print line
	# 			return
	# print "No record found"


	# print database[1]
	# if len(argv) == 1:
	# 	lookupName = argv[0]
	# 	print len(database)
	# 	for line in database:
	# 		if lookupName in (line["player1"], line["player2"]):
	# 			print line
	# 			return
	# 	print "No record found"
	# 	return

	# print "Database created"

			# if line["player1"] == lookupName or line["player2"] == lookupName:
			# 	print "hello me"




if __name__ == '__main__':
	main(sys.argv[1:])
	# saveTest();
	



	# i = 1
	# string = linesList[259].strip()
	# if string == "<td>%s</td>" % (i):
	# 	print "hello"
# this is working
	# for i in range(len(linesList)):
	# 	currentString = linesList[i]
	# 	if profileStr in currentString:
	# 		print currentString

	# for i in range(len(linesList)):
	# 	currentString = linesList[i]
	# 	print linesList[1]
	# 	if currentString.startswith(profileStr):
	# 		print "current string:"
	# 		print currentString
	# 		print i
	# 		exit()
