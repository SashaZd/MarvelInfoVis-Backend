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