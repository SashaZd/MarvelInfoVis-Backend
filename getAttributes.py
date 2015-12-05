import json
import re


listOfCharsFiles = open("data/charactersList.txt")
CHAR_BASE_LINK = "data/characters/"
COMICS_BASE_LINK = "data/comics/"
wikiData = json.loads(open("data/wikiData.json").read())



def getAllRelationships():
	charRels = {}

	for eachCharFile in listOfCharsFiles:
		filePath = CHAR_BASE_LINK+eachCharFile.strip()
		charData = json.loads(open(filePath).read())
		
		char_id = charData["id"]
		
		if "wiki" in charData and "relatives" in charData["wiki"]:
			charRels[char_id] = {
				"name": charData["name"],
				"relatives": charData["wiki"]["relatives"]
			}


	tempRelationshipFile = open("relationship.json","w")
	tempRelationshipFile.write(json.dumps(charRels))	


# To do
def getAllComicsData():
	listOfComicFiles = open("data/allComics.txt")






def getAffiliationMembers():
	affilationList = json.loads(open("data/affiliations_all.json").read())
	charAffs = {}

	for eachCharFile in listOfCharsFiles:	
		filePath = CHAR_BASE_LINK+eachCharFile.strip()
		charData = json.loads(open(filePath).read())
		affiliation = []

		char_id = charData["id"]
		char_name = []
		char_name.append(charData["name"])

		if "wiki" in charData and "real_name" in charData["wiki"]:
			char_name.append(charData["wiki"]["real_name"])

		found = [charName for charName in char_name if charName in wikiData]
		print char_id
		if len(found) > 0:
			for eachAffiliation in affilationList: 
				if "Affiliation" in wikiData[found[0]]:
					if eachAffiliation in wikiData[found[0]] and eachAffiliation not in affiliation:
						affiliation.append(eachAffiliation)

				if "wiki" in charData and "groups" in charData["wiki"]:
					if eachAffiliation in charData["wiki"]["groups"] and eachAffiliation not in affiliation: 
						affiliation.append(eachAffiliation)

				if "wiki" in charData and "categories" in charData["wiki"] and charData["wiki"]["categories"] is not None and len(charData["wiki"]["categories"]) > 0:
					if eachAffiliation in charData["wiki"]["categories"] and eachAffiliation not in affiliation:
						affiliation.append(eachAffiliation)

		charAffs[char_id]=affiliation

	affiliation_members = open("data/affiliation_members.json", "w")
	affiliation_members.write(json.dumps(charAffs))	


def getAllGenders():
	genders = {}

	for eachCharFile in listOfCharsFiles:
		filePath = CHAR_BASE_LINK+eachCharFile.strip()
		charData = json.loads(open(filePath).read())
		gender = "Unknown"

		char_id = charData["id"]
		char_name = []
		char_name.append(charData["name"])

		if "wiki" in charData and "real_name" in charData["wiki"]:
			char_name.append(charData["wiki"]["real_name"])

		found = [charName for charName in char_name if charName in wikiData]
		
		if len(found) > 0:
			# print wikiData[found[0]]
			if "Gender" in wikiData[found[0]]:
				gender = wikiData[found[0]]["Gender"]

		genders[char_id] = gender

	gender_file = open("data/genders.json", "w")
	gender_file.write(json.dumps(genders))	




def getAllOriginYears():
	originList = {}

	for eachCharFile in listOfCharsFiles: 
		filePath = CHAR_BASE_LINK+eachCharFile.strip()
		charData = json.loads(open(filePath).read())
		year = ""

		if "wiki" in charData and "debut" in charData["wiki"] and charData["wiki"]["debut"] != "":
			if "(" in charData["wiki"]["debut"]:
				yearTemp = re.split("\(|\)", charData["wiki"]["debut"])[1]
				if yearTemp.isdigit(): 
					year = yearTemp
			else:
				year = re.split(",|;", charData["wiki"]["debut"])[0].strip()
		elif "wiki" in charData and "origin" in charData["wiki"] and charData["wiki"]["origin"] != "":
			if "(" in charData["wiki"]["origin"]:
				yearTemp = re.split("\(|\)", charData["wiki"]["origin"])[1]
				if yearTemp.isdigit(): 
					year = yearTemp
			else:
				year = re.split(",|;", charData["wiki"]["origin"])[0].strip()
		else: 
			year = "Unknown"

		originList[charData["id"]] = year

	listOfOriginsFile = open("data/origins_members.txt", "w")
	listOfOriginsFile.write(json.dumps(originList))	


def getAllUniqueCitizenships():
	listOfCharsFiles = open("data/charactersList.txt")
	CHAR_BASE_LINK = "data/characters/"
	all_citizens = json.loads(open("data/citizenships_all.txt").read())

	citizenships = []
	citizenships_List = {}

	for eachCharFile in listOfCharsFiles: 
		filePath = CHAR_BASE_LINK+eachCharFile.strip()
		charData = json.loads(open(filePath).read())

		citizenships_List[charData["id"]] = []

		if "wiki" in charData and "citizenship" in charData["wiki"]:
			if charData["wiki"]["citizenship"] not in citizenships:
				tempCiti = charData["wiki"]["citizenship"]
				for eachCiti in all_citizens:
					if eachCiti in tempCiti:
						citizenships_List[charData["id"]].append(eachCiti)
		else: 
			citizenships_List[charData["id"]].append("Unknown")

	print citizenships_List

	listOfCitizenshipsFile = open("data/citizenships_members.txt", "w")
	listOfCitizenshipsFile.write(json.dumps(citizenships_List))


def getAllUniqueAffiliations(): 
	# Some manual cleaning up of the data was also done. So do not run this again unless absolutely necessary
	listOfAffiliations = []
	for eachCharFile in listOfCharsFiles: 
		filePath = CHAR_BASE_LINK+eachCharFile.strip()

		charFile = open(filePath).read()
		data = json.loads(charFile)

		if "wiki" in data and "groups" in data["wiki"]:
			affiliations = data["wiki"]["groups"].split(",")

			for eachAffiliation in affiliations:
				if eachAffiliation.strip() not in listOfAffiliations and eachAffiliation != "" and eachAffiliation != None:
					check = re.split("\\\"|\[\[|\]\]", eachAffiliation.strip())[1::2]
					if len(check) > 0:
						listOfAffiliations.extend(check)

		if "wiki" in data and "categories" in data["wiki"]:
			affiliations = data["wiki"]["categories"]
			if affiliations:
				for eachAffiliation in affiliations:
					if eachAffiliation.strip() not in listOfAffiliations and eachAffiliation != "" and eachAffiliation != None:
						listOfAffiliations.append(eachAffiliation.strip())
					
	listOfAffiliations = list(set(listOfAffiliations))
	listOfAffiliationsFile = open("affiliations.txt", "w")
	listOfAffiliationsFile.write(json.dumps(listOfAffiliations))



# getAllRelationships()





