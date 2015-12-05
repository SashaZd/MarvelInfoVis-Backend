# Common Imports for all Manager Files 
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime, timedelta


# Other Imports
from ..models import Affiliations, Character, Relationship


@csrf_exempt
def setGenders(request):
	response_data = []

	response_data = {"warning":"You're resetting all the genders in the database with this command. If you want to continue, uncomment the entire function setGenders in CharacterManager, and comment out this line"}
	
	# allChars = Character.objects.all()
	# if len(allChars) > 0:
	# 	for eachAffiliation in allChars:
	# 		response_data.append(eachAffiliation.setGender())
	# 		# response_data.append(eachAffiliation.name)
	# else: 
		# response_data = {"error":"There's no data in the Character Table. Did you wipe the database? Uncomment and Run the Affiliations script at the bottom of models.py after the first time you run makemigrations."}
	return HttpResponse(json.dumps(response_data), content_type="application/json")

def setAffiliation(request):
	response_data = []
	
	response_data = {"warning":"You're resetting all the affiliations in the database with this command. If you want to continue, uncomment the entire function setAffiliation in CharacterManager, and comment out this line"}

	# allChars = Character.objects.all()
	# if len(allChars) > 0:
	# 	for eachAffiliation in allChars:
	# 		eachAffiliation.setAffiliation()
	# 		response_data.append(eachAffiliation.name)
	# else: 
	# 	response_data = {"error":"There's no data in the Character Table. Did you wipe the database? Uncomment and Run the Affiliations script at the bottom of models.py after the first time you run makemigrations."}

	return HttpResponse(json.dumps(response_data), content_type="application/json")

def setRelations(request):
	response_data = []

# Temporary List of Relationships. Just Family/Core Relationships. No love or anything marked out
	# listOfCharsFiles = open("data/charactersList.txt")
	# CHAR_BASE_LINK = "data/characters/"
	# allChars = Character.objects.all()


	# for eachCharFile in listOfCharsFiles:
	# 	filePath = CHAR_BASE_LINK+eachCharFile.strip()
	# 	charData = json.loads(open(filePath).read())

	# 	charRels = {}
	# 	relatives = []
	# 	firstPersonChar = Character.objects.filter(character_id=charData["id"])[0]

	# 	if "wiki" in charData and "relatives" in charData["wiki"]:
	# 		for eachChar in allChars:
	# 			flagAdd = False
	# 			if eachChar.name in charData["name"] and eachChar.character_id != charData["id"]: 
	# 				flagAdd = True
	# 			elif "real_name" in charData["wiki"] and eachChar.name in charData["wiki"]["real_name"] and eachChar.character_id != charData["id"]: 
	# 				flagAdd = True
	# 			elif "aliases" in charData["wiki"] and eachChar.name in charData["wiki"]["aliases"] and eachChar.character_id != charData["id"]: 
	# 				flagAdd = True

	# 			if flagAdd == True:
	# 				relatives.append({
	# 					"name": eachChar.name,
	# 					"id": eachChar.character_id 
	# 				})

	# 				relationship, created = Relationship.objects.get_or_create(from_person=firstPersonChar, to_person=eachChar, relationship_type="Family")
	# 				# print "Connected ", firstPersonChar.name, " -----> ", eachChar.name

	# 		if len(relatives)!=0:
	# 			charRels = {
	# 				"id": charData["id"],
	# 				"name": charData["name"],
	# 				"relatives": relatives
	# 			}
	# 			response_data.append(charRels)

					
	response_data = {"warning":"You're resetting all the relationships in the database with this command. If you want to continue, uncomment the entire function setRelations in CharacterManager, and comment out this line"}

	return HttpResponse(json.dumps(response_data), content_type="application/json")





