# Common Imports for all Manager Files 
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.db.models import Count

# Other Imports
from ..models import Affiliations, Character, Relationship


@csrf_exempt

@csrf_exempt
def nationalityRequest(request):
	if request.method == "GET":
		return getAllNationalities(request)

	else: 
		return getNationalityByName(request)

def affiliationRequest(request):
	if request.method == "GET":
		# Return list of affiliations only
		return getAllAffiliations(request)

	else:
		# Returns a specific affiliation with it's members as charObjs
		return getAffiliationByName(request)


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

	print len(charsByNation)

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
