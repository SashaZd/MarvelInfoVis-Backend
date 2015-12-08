# Common Imports for all Manager Files 
import json, random
from sets import Set
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


@csrf_exempt
def filterAll(request):
	if request.method == "POST":
		return useAllFilters(request)


@csrf_exempt
def getCommonRandomComic(request):
	if request.method == "POST":
		return getRandomCommonComicForChars(request)

#################################
# Redirected Methods Below
#################################

def getRandomCommonComicForChars(request):
	response_data = {}

	firstChar = request.POST.get('firstChar', None)
	secondChar = request.POST.get('secondChar', None)

	if not firstChar and not secondChar: 
		allComics = Comic.objects.all()
		response_data = random.choice(allComics).getResponseData()

	elif firstChar and not secondChar:
		firstChar = Character.objects.filter(character_id=firstChar)
		comics = Comic.objects.filter(character=firstChar)
		response_data = random.choice(comics).getResponseData()

	elif firstChar and secondChar: 
		firstChar = Character.objects.filter(character_id=firstChar)
		secondChar = Character.objects.filter(character_id=secondChar)
		comics = Comic.objects.filter(character=firstChar).filter(character=secondChar)
		response_data = random.choice(comics).getResponseData()

	return HttpResponse(json.dumps(response_data), content_type="application/json")



def useAllFilters(request):

	response_data = {}
	response_data["characters"] = []
	response_data["filters"] = {}
	response_data["filters"]["gender"] = []
	response_data["filters"]["nationality"] = []
	response_data["filters"]["appearances"] = []
	response_data["filters"]["intro_year"] = []
	response_data["filters"]["affiliations"] = []

	name = request.POST.get('name', None)
	appearances_min = request.POST.get('appearances_min', None)
	appearances_max = request.POST.get('appearances_max', None)
	gender = request.POST.get('gender', None)
	nationality = request.POST.get('nationality', None)
	intro_year_min = request.POST.get('intro_year_min', None)
	intro_year_max = request.POST.get('intro_year_max', None)
	affiliation = request.POST.get('affiliation', None)

	if not name and not appearances_min and not appearances_max and not gender and not nationality and not intro_year_min and not intro_year_max and not affiliation:
		return getAllCharactersFromDB()

	set_name, name_flag = utilFilterName(name)
	set_affiliation, affiliation_flag = utilFilterAffiliation(affiliation)
	set_gender, gender_flag = utilFilterGender(gender)
	set_nationality, nationality_flag = utilFilterNationality(nationality)
	set_appearance = utilFilterAppearances(appearances_min, appearances_max)
	set_introYear = utilFilterIntroYear(intro_year_min, intro_year_max)
	
	


	allChars = Character.objects.all()
	universalSet = set()
	for eachChar in allChars:
		universalSet.add(eachChar.id)

	if name_flag:
		universalSet = universalSet & set_name
	if affiliation_flag: 
		universalSet = universalSet & set_affiliation
	if gender_flag:
		universalSet = universalSet & set_gender
	if nationality_flag:
		universalSet = universalSet & set_nationality
	
	universalSet = universalSet & set_appearance & set_introYear
	universalSet = list(universalSet)

	shortlistedChars = Character.objects.filter(id__in=universalSet)
	responseData = utilShortlistedBuildResponse(response_data, shortlistedChars)
	

	return HttpResponse(json.dumps(response_data), content_type="application/json")


#####################################################
#####################################################
#####################################################

def utilShortlistedBuildResponse(response_data, shortlistedChars):
	for eachChar in shortlistedChars:
		response_data["characters"].append(eachChar.getResponseData())
		if eachChar.gender not in response_data["filters"]["gender"]:
			response_data["filters"]["gender"].append(eachChar.gender)
		if eachChar.nationality not in response_data["filters"]["nationality"]:
			response_data["filters"]["nationality"].append(eachChar.nationality)
		if eachChar.appearances not in response_data["filters"]["appearances"]:
			response_data["filters"]["appearances"].append(eachChar.appearances)
		if eachChar.intro_year not in response_data["filters"]["intro_year"]:
			response_data["filters"]["intro_year"].append(eachChar.intro_year)
		
		for eachAffiliation in eachChar.affiliations.all():
			if eachAffiliation.title not in response_data["filters"]["affiliations"]:
				response_data["filters"]["affiliations"].append(eachAffiliation.title)

	return response_data

def utilFilterName(name):
	set_name = set()
	name_flag = False

	if name:
		name_filteredChars = Character.objects.filter(name__icontains=name)
		name_flag = True
		for eachChar in name_filteredChars:
			set_name.add(eachChar.id)

	return set_name, name_flag


def utilFilterAffiliation(affiliation):
	set_affiliation = set()
	affiliation_flag = False

	if affiliation: 
		affiliation_filteredChars = Affiliations.objects.filter(title__icontains=affiliation)
		for eachAffiliation in affiliation_filteredChars:
			characters = eachAffiliation.character_set.all()
			for eachChar in characters:
				set_affiliation.add(eachChar.id)
		affiliation_flag = True

	return set_affiliation, affiliation_flag


def utilFilterGender(gender):
	set_gender = set()
	gender_flag = False

	if gender:
		gender_filteredChars = Character.objects.filter(gender=gender)
		gender_flag = True
		for eachChar in gender_filteredChars:
			set_gender.add(eachChar.id)

	return set_gender, gender_flag


def utilFilterNationality(nationality):
	set_nationality = set()
	nationality_flag = False

	if nationality:
		nationality_filteredChars = Character.objects.filter(nationality__icontains=nationality)
		nationality_flag = True
		for eachChar in nationality_filteredChars:
			set_nationality.add(eachChar.id)

	return set_nationality, nationality_flag

def utilFilterAppearances(appearances_min, appearances_max):
	set_appearance = set()

	if not appearances_min:
		appearances_min = Character.objects.aggregate(Min('appearances'))["appearances__min"]
	if not appearances_max: 
		appearances_max = Character.objects.aggregate(Max('appearances'))["appearances__max"]

	appearances_filteredChars = Character.objects.filter(appearances__range=(appearances_min, appearances_max))
	for eachChar in appearances_filteredChars:
		set_appearance.add(eachChar.id)

	return set_appearance


def utilFilterIntroYear(intro_year_min, intro_year_max):
	set_introYear = set()

	if not intro_year_min:
		intro_year_min = Character.objects.aggregate(Min('intro_year'))["intro_year__min"]
	if not intro_year_max: 
		intro_year_max = Character.objects.aggregate(Max('intro_year'))["intro_year__max"]

	intro_year_filteredChars = Character.objects.filter(intro_year__range=(intro_year_min, intro_year_max))
	for eachChar in intro_year_filteredChars:
		set_introYear.add(eachChar.id)

	return set_introYear



#####################################################
#####################################################
#####################################################

def getAllCharactersFromDB():
	response_data = {}
	response_data["characters"] = []
	response_data["filters"] = {}
	response_data["filters"]["gender"] = []
	response_data["filters"]["nationality"] = []
	response_data["filters"]["appearances"] = []
	response_data["filters"]["intro_year"] = []
	response_data["filters"]["affiliations"] = []
	allChars = Character.objects.all()

	for eachChar in allChars:
		response_data["characters"].append(eachChar.getResponseData())
		if eachChar.gender not in response_data["filters"]["gender"]:
			response_data["filters"]["gender"].append(eachChar.gender)
		if eachChar.nationality not in response_data["filters"]["nationality"]:
			response_data["filters"]["nationality"].append(eachChar.nationality)
		if eachChar.appearances not in response_data["filters"]["appearances"]:
			response_data["filters"]["appearances"].append(eachChar.appearances)
		if eachChar.intro_year not in response_data["filters"]["intro_year"]:
			response_data["filters"]["intro_year"].append(eachChar.intro_year)
		
		for eachAffiliation in eachChar.affiliations.all():
			if eachAffiliation.title not in response_data["filters"]["affiliations"]:
				response_data["filters"]["affiliations"].append(eachAffiliation.title)

	return HttpResponse(json.dumps(response_data), content_type="application/json")


def getCharacterById(request):
	response_data = []
	character_id = request.POST.get('character_id','')

	findChars = Character.objects.filter(character_id=character_id)
	if len(findChars) > 0:
		character = findChars[0]
		response_data = character.getResponseData()

		comics = Comic.objects.filter(character=character)
		if len(comics) > 0:
			response_data["comic"] = random.choice(comics).getResponseData()

		affiliations = Affiliations.objects.filter(character=character)
		response_data["affiliations"] = []
		for eachAffiliation in affiliations:
			response_data["affiliations"].append(eachAffiliation.title)

	else:
		response_data = {error:"Warning: Hydra Infiltration. Page unavailable while attack under enemy forces. \nMake sure you typed in the correct character_id and resend this request"}

	return HttpResponse(json.dumps(response_data), content_type="application/json")

def getConnectionsForCharById(request):
	response_data = []
	character_id = request.POST.get('character_id', '')

	fromPerson = Character.objects.filter(character_id=character_id)

	toPeople = Relationship.objects.filter(from_person=fromPerson)
	fromPeople = Relationship.objects.filter(to_person=fromPerson)

	toAllPeople = set()

	for eachRelationship in toPeople: 
		toAllPeople.add(eachRelationship.id)
	for eachRelationship in fromPeople:
		toAllPeople.add(eachRelationship.id)

	toAllPeople = list(toAllPeople)
	allConnections = Relationship.objects.filter(id__in=toAllPeople)
	print len(allConnections)

	for eachRelationship in allConnections:
		otherPerson = ""
		if eachRelationship.from_person == fromPerson: 
			otherPerson = eachRelationship.to_person
		else:
			otherPerson = eachRelationship.from_person

		print otherPerson.name
		if eachRelationship.strength > 0:
			comic = Comic.objects.filter(character=fromPerson).filter(character=otherPerson)[0].getResponseData()
			print comic["title"]
		else:
			comic = {}

		connection = {
			"cid1": character_id,
			"cid2": str(eachRelationship.to_person.character_id),
			"type": eachRelationship.relationship_type,
			"instances": eachRelationship.strength,
			"comic": comic
		}

		response_data.append(connection)


	# for eachRelationship in toPeople:
	# 	if eachRelationship.strength > 0:
	# 		comic = random.choice(Comic.objects.filter(character=fromPerson).filter(character=eachRelationship))

	# 	connection = {
	# 		"cid1": character_id,
	# 		"cid2": str(eachRelationship.to_person.character_id),
	# 		"type": eachRelationship.relationship_type,
	# 		"instances": eachRelationship.strength
	# 	}
	# 	response_data.append(connection)

	# for eachRelationship in fromPeople:

	# 	connection = {
	# 		"cid1": character_id,
	# 		"cid2": str(eachRelationship.from_person.character_id),
	# 		"type": eachRelationship.relationship_type,
	# 		"instances": eachRelationship.strength
	# 	}
	# 	if connection not in response_data:
	# 		response_data.append(connection)

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



