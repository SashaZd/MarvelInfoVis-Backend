# Common Imports for all Manager Files 
import json, itertools
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime, timedelta


# Other Imports
from ..models import Affiliations, Character, Relationship, Comic


@csrf_exempt
def setComicConnections(request):
	response_data = []


	response_data = {"warning":"You're trying to recount the relationship strength between characters. This takes 11hrs! If you want to continue, uncomment the entire function setComicChars in CharacterManager, and comment out this line"}
	# strengthData = json.loads(open("data/RelationshipStrengths.json").read())

	# for eachRelationship in strengthData: 
	# 	# print eachRelationship, strengthData[eachRelationship]
	# 	firstChar, secondChar = eachRelationship.split(":")

	# 	firstPersonChar = Character.objects.filter(id=firstChar)[0]
	# 	secondPersonChar = Character.objects.filter(id=secondChar)[0]

	# 	relationship, created = Relationship.objects.get_or_create(from_person=firstPersonChar, to_person=secondPersonChar, relationship_type="Family")
	# 	if created == True: 
	# 		relationship.relationship_type = "Standard"
	# 	else:
	# 		relationship.relationship_type = "Family"

	# 	relationship.strength = int(strengthData[eachRelationship]) | 1
	# 	relationship.save()
	# 	print firstPersonChar.name, " --- ", secondPersonChar.name

	return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def setConnectionCounts(request):
	response_data = []

	response_data = {"warning":"You're trying to recount the relationship strength between characters. This takes 11hrs! If you want to continue, uncomment the entire function setComicChars in CharacterManager, and comment out this line"}
	# allRelationships = {}

	# for eachComic in Comic.objects.all():
	# 	allParticipatingChars = eachComic.character_set.all()
		

	# 	for eachRelationship in itertools.combinations(allParticipatingChars, 2):
	# 		key = str(eachRelationship[0].id) + ":" + str(eachRelationship[1].id)
	# 		if key in allRelationships:
	# 			allRelationships[key] = allRelationships[key] + 1
	# 		else:
	# 			allRelationships[key] = 1

	# 	print eachComic.id, eachComic.title

	# tempOutPut = open("RelationshipStrengths.json", "w")
	# tempOutPut.write(json.dumps(allRelationships))	

	return HttpResponse(json.dumps(allRelationships), content_type="application/json")

def setComicChars(request):
	response_data = []

	response_data = {"warning":"You're trying to add all the comics into the database from scratch. This takes 11hrs! If you want to continue, uncomment the entire function setComicChars in CharacterManager, and comment out this line"}

	# allChars = Character.objects.all()
	# if len(allChars) > 0:
	# 	for eachChar in allChars:
	# 		eachChar.setComics()
	# 		response_data.append(eachChar.name)
	# else: 
	# 	response_data = {"error":"There's no data in the Character Table. Did you wipe the database? Uncomment and Run the Affiliations script at the bottom of models.py after the first time you run makemigrations."}

	# print "Added EVERY Comic in"

	return HttpResponse(json.dumps(response_data), content_type="application/json")


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
	# 			if eachChar.name in charData["wiki"]["relatives"] and eachChar.character_id != charData["id"]: 
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





