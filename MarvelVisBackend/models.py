from django.db import models
import json, re

class Affiliations(models.Model):
	title = models.CharField(max_length=50)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ('title',)


class Character(models.Model):
	character_id = models.CharField(max_length=10)
	name = models.CharField(max_length=30)
	appearances = models.CharField(max_length=10)
	gender = models.CharField(max_length=30)
	nationality = models.CharField(max_length=50)
	intro_year = models.CharField(max_length=10)
	image = models.CharField(max_length=100)
	bio_desc = models.CharField(max_length=150)

	# Relationships & Many-Many Fields 
	affiliations = models.ManyToManyField(Affiliations)
	relationships = models.ManyToManyField('self', through='Relationship', symmetrical=False, related_name='related_to')

	# def __init__(self, character_id, name, appearances, gender, nationality, intro_year, image, bio_desc):
	# 	self.character_id = character_id
	# 	self.name = name
	# 	self.appearances = appearances
	# 	self.gender = gender
	# 	self.nationality = nationality
	# 	self.intro_year = intro_year
	# 	self.image = image
	# 	self.bio_desc = bio_desc

	def __unicode__(self):
		name = self.name
		return name

	def getResponseData(self):
		#Create Resposne Dictionary
		response_data = {}
		response_data["character_id"] = self.character_id
		response_data["name"] = self.name
		response_data["name"] = self.name
		response_data["appearances"] = self.appearances
		response_data["gender"] = self.gender
		response_data["nationality"] = self.nationality
		response_data["intro_year"] = self.intro_year
		response_data["bio_desc"] = self.bio_desc
		response_data["image"] = self.image
		
		return response_data

	def setAffiliation(self):
		allChars = json.loads(open("data/affiliation_members.json").read())
		# self.gender = allChars[str(self.character_id)][0].strip()
		# self.save()

		affiliations_list = allChars[str(self.character_id)]
		# return affiliations_list

		for eachAffiliation in affiliations_list:
			self.affiliations.add(Affiliations.objects.filter(title=eachAffiliation)[0])
		
		self.save()

	def setGender(self):
		allChars = json.loads(open("data/genders.json").read())
		self.gender = allChars[str(self.character_id)][0].strip()
		self.save()

class Relationship(models.Model):
	from_person = models.ForeignKey(Character, related_name='from_people')
	to_person = models.ForeignKey(Character, related_name='to_people')
	relationship_type = models.CharField(max_length=50)



######################

# For New DB/Tables, after deleting the database uncomment this and run it ONCE after you run migrate the first time.


"""
# For Affiliations Table: 
listOfAffilitations = json.loads(open("data/affiliations_all.json").read())
for eachAffiliation in listOfAffilitations:
	newAff = Affiliations(title=eachAffiliation.strip())
	newAff.save()
"""

"""
# For Character Table: 
listOfCharsFiles = open("data/charactersList.txt")
citizenship_members = json.loads(open("data/citizenships_members.txt").read())
origins_members = json.loads(open("data/origins_members.txt").read())
CHAR_BASE_LINK = "data/characters/"

for eachCharFile in listOfCharsFiles: 
	filePath = CHAR_BASE_LINK+eachCharFile.strip()
	charData = json.loads(open(filePath).read())
	
	thumbnail = charData["thumbnail"]["path"]+"."+charData["thumbnail"]["extension"]
	bio_desc = "",
	nationality_list = citizenship_members[str(charData["id"])]
	nationality = ', '.join(str(e) for e in nationality_list)

	if "wiki" in charData: 
		if "blurb" in charData["wiki"]: 
			bio_desc = charData["wiki"]["blurb"]
		elif "bio_text" in charData["wiki"]:
			bio_desc = charData["wiki"]["bio_text"]
		elif "bio" in charData["wiki"]:
			bio_desc = charData["wiki"]["bio"]

	newChar = Character(
		character_id= charData["id"],
		name= charData["name"],
		appearances= charData["comics"]["available"],
		gender= "Unknown",
		nationality= nationality,
		intro_year= origins_members[str(charData["id"])],
		image= thumbnail,
		bio_desc= bio_desc
		);

	newChar.save()
"""	



