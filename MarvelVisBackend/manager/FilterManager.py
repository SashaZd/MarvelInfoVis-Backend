# Common Imports for all Manager Files 
import json, random
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime, timedelta

from django.db.models import Count
from django.db.models import Avg, Max, Min

# Other Imports
from ..models import Affiliations, Character, Relationship, Comic


@csrf_exempt
def genderRequest(request):
	if request.method == "GET":
		return getAllGenders(request)

	else: 
		return getGenderByName(request)

@csrf_exempt
def yearIntroducedRequest(request):
	if request.method == "GET":
		return getAllYearsIntroduced(request)

	else: 
		return getYearIntroducedByYear(request)

@csrf_exempt
def nationalityRequest(request):
	if request.method == "GET":
		return getAllNationalities(request)

	else: 
		return getNationalityByName(request)

@csrf_exempt
def affiliationRequest(request):
	if request.method == "GET":
		# Return list of affiliations only
		return getAllAffiliations(request)

	else:
		# Returns a specific affiliation with it's members as charObjs
		return getAffiliationByName(request)

@csrf_exempt
def appearancesRange(request):
	if request.method == "POST":
		return getAppearancesWithinRange(request)

@csrf_exempt
def connectionsForChar(request):
	if request.method == "POST":
		return getConnectionsForCharById(request)

@csrf_exempt
def getDetailedCharacter(request):
	if request.method == "POST":
		return getCharacterById(request)


#################################
# Redirected Methods Below
#################################

def getCharacterById(request):
	response_data = []
	character_id = request.POST.get('character_id','')

	findChars = Character.objects.filter(character_id=character_id)
	if len(findChars) > 0:
		character = findChars[0]
		response_data = character.getResponseData()

		comics = Comic.objects.filter(character=character)
		response_data["comic"] = random.choice(comics).getResponseData()

		affiliations = Affiliations.objects.filter(character=character)
		response_data["affiliations"] = []
		for eachAffiliation in affiliations:
			response_data["affiliations"].append(eachAffiliation.title)
		


	return HttpResponse(json.dumps(response_data), content_type="application/json")

def getConnectionsForCharById(request):
	response_data = []
	character_id = request.POST.get('character_id', '')

	fromPerson = Character.objects.filter(character_id=character_id)

	toPeople = Relationship.objects.filter(from_person=fromPerson)
	fromPeople = Relationship.objects.filter(to_person=fromPerson)

	for eachRelationship in toPeople:
		connection = {
			"cid1": character_id,
			"cid2": str(eachRelationship.to_person.character_id),
			"type": eachRelationship.relationship_type,
			"instances": eachRelationship.strength
		}
		response_data.append(connection)

	for eachRelationship in fromPeople:
		connection = {
			"cid1": character_id,
			"cid2": str(eachRelationship.from_person.character_id),
			"type": eachRelationship.relationship_type,
			"instances": eachRelationship.strength
		}
		if connection not in response_data:
			response_data.append(connection)

	return HttpResponse(json.dumps(response_data), content_type="application/json")

def getAppearancesWithinRange(request):
	startRange = request.POST.get('startRange','')
	endRange = request.POST.get('endRange','')

	if startRange == '':
		startRange = Character.objects.aggregate(Min('appearances'))["appearances__min"]

	if endRange == '': 
		endRange = Character.objects.aggregate(Max('appearances'))["appearances__max"]

	response_data = []

	appearances = Character.objects.filter(appearances__range=(startRange, endRange))

	members = []
	for eachChar in appearances:
		members.append(eachChar.getResponseData())

	if len(members) > 0:
		response_data.extend(members)

	return HttpResponse(json.dumps(response_data), content_type="application/json")


def getAllGenders(request):
	response_data = []

	genders = Character.objects.all().values("gender").distinct().annotate(number=Count("id"))

	for eachGender in genders: 
		response_data.append(eachGender)

	return HttpResponse(json.dumps(response_data), content_type="application/json")


def getGenderByName(request):
	response_data = []
	gender =  request.POST.get('gender','')

	charsByGender = Character.objects.filter(gender=gender)

	members = []
	for eachChar in charsByGender:
		members.append(eachChar.getResponseData())

	if len(members) > 0:
		response_data.extend(members)

	return HttpResponse(json.dumps(response_data), content_type="application/json")



def getAllYearsIntroduced(request):
	response_data = []

	allYears = Character.objects.all().values("intro_year").distinct().annotate(number=Count("id"))

	for eachYear in allYears: 
		response_data.append(eachYear)

	return HttpResponse(json.dumps(response_data), content_type="application/json")


def getYearIntroducedByYear(request):
	response_data = []
	name =  request.POST.get('year','')

	charsByYear = Character.objects.filter(intro_year__icontains=name)

	members = []
	for eachChar in charsByYear:
		members.append(eachChar.getResponseData())

	if len(members) > 0:
		response_data.extend(members)

	return HttpResponse(json.dumps(response_data), content_type="application/json")



def getAllNationalities(request):
	response_data = []

	allNationalities = Character.objects.all().values("nationality").distinct().annotate(number=Count("id"))

	for eachNationality in allNationalities: 
		response_data.append(eachNationality)

	return HttpResponse(json.dumps(response_data), content_type="application/json")


def getNationalityByName(request):
	response_data = []
	name =  request.POST.get('name','')

	charsByNation = Character.objects.filter(nationality__icontains=name)

	members = []
	for eachChar in charsByNation:
		members.append(eachChar.getResponseData())

	if len(members) > 0:
		response_data.extend(members)

	return HttpResponse(json.dumps(response_data), content_type="application/json")


def getAllAffiliations(request):
	response_data = []
	allAffiliations = Affiliations.objects.all()

	if len(allAffiliations) > 0:
		for eachAffiliation in allAffiliations: 
			response_data.append(eachAffiliation.getResponseData())

	else: 
		response_data = {"error":"No affiliations in the database."}

	return HttpResponse(json.dumps(response_data), content_type="application/json")


def getAffiliationByName(request):
	response_data = []
	name =  request.POST.get('name','')

	allAffiliations = Affiliations.objects.filter(title__icontains=name)

	if len(allAffiliations) > 0:
		for eachAffiliation in allAffiliations:
			chars = eachAffiliation.character_set.all()
			members = []
			for eachChar in chars: 
				members.append(eachChar.getResponseData())

			if len(members) > 0:
				newAffObj = {
					"affiliation": eachAffiliation.title,
					"members": members
				}
				response_data.append(newAffObj)

	else: 
		response_data = {"error":"There's no data in the Affiliations Table. Did you wipe the database? Uncomment and Run the Affiliations script at the bottom of models.py after the first time you run makemigrations."}
	
	return HttpResponse(json.dumps(response_data), content_type="application/json")


"""
Default Method: 
def defaultMethod(request):
	response_data = []

	return HttpResponse(json.dumps(response_data), content_type="application/json")
"""



