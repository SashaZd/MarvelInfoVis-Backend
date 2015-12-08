from django.db import models
import json, re

class Affiliations(models.Model):
	title = models.CharField(max_length=50)

	def __str__(self):
		return self.title

	def getResponseData(self):
		return self.title.strip()

	class Meta:
		ordering = ('title',)



class Comic(models.Model):
	comic_id = models.CharField(max_length=10)
	title = models.CharField(max_length=50)
	description = models.CharField(max_length=150)
	image = models.CharField(max_length=100)
	details_url = models.CharField(max_length=100)
	purchase_url = models.CharField(max_length=100)
	price_digital = models.CharField(max_length=10)
	price_print = models.CharField(max_length=10)

	def __unicode__(self):
		return self.title

	def getResponseData(self):
		#Create Resposne Dictionary
		response_data = {}
		response_data["comic_id"] = self.comic_id
		response_data["title"] = self.title
		response_data["description"] = self.description
		response_data["image"] = self.image
		response_data["details_url"] = self.details_url
		response_data["purchase_url"] = self.purchase_url
		response_data["price_digital"] = self.price_digital
		response_data["price_print"] = self.price_print
		
		return response_data



class Character(models.Model):
	character_id = models.CharField(max_length=10)
	name = models.CharField(max_length=30)
	appearances = models.CharField(max_length=10)
	gender = models.CharField(max_length=30)
	nationality = models.CharField(max_length=50)
	intro_year = models.CharField(max_length=10)
	image = models.CharField(max_length=100)
	bio_desc = models.CharField(max_length=150)
	aliases = models.CharField(max_length=150)
	url = models.CharField(max_length=150)

	# Relationships & Many-Many Fields 
	affiliations = models.ManyToManyField(Affiliations)
	comics = models.ManyToManyField(Comic)
	relationships = models.ManyToManyField('self', through='Relationship', symmetrical=False, related_name='related_to')

	def __unicode__(self):
		name = self.name
		return name

	def getResponseData(self):
		#Create Resposne Dictionary
		response_data = {}
		response_data["character_id"] = self.character_id
		response_data["name"] = self.name
		response_data["appearances"] = self.appearances
		response_data["gender"] = self.gender
		response_data["nationality"] = self.nationality
		response_data["intro_year"] = self.intro_year
		response_data["bio_desc"] = self.bio_desc
		response_data["image"] = self.image
		response_data["aliases"] = self.aliases
		response_data["url"] = self.url
		
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

	def setComics(self):
		charUrl = "data/characters/"+str(self.character_id)+".json"
		charData = json.loads(open(charUrl).read())

		if "comics" in charData and "items" in charData["comics"] and len(charData["comics"]["items"]) > 0:
			for eachComic in charData["comics"]["items"]:
				if "id" in eachComic and len(Comic.objects.filter(comic_id=eachComic["id"])) > 0:
					self.comics.add(Comic.objects.filter(comic_id=eachComic["id"])[0])

					print self.name, " ----> ", Comic.objects.filter(comic_id=eachComic["id"])[0].title
		self.save()


class Relationship(models.Model):
	from_person = models.ForeignKey(Character, related_name='from_people')
	to_person = models.ForeignKey(Character, related_name='to_people')
	relationship_type = models.CharField(max_length=50)
	strength = models.CharField(max_length=50)

	def __unicode__(self):
		name = self.from_person.name + " -- " + self.relationship_type + " -- " + self.to_person.name
		return name

	def getResponseData(self):
		#Create Resposne Dictionary
		response_data = {}
		response_data["from_person"] = self.from_person
		response_data["to_person"] = self.to_person
		response_data["relationship_type"] = self.relationship_type
		response_data["strength"] = self.strength
		
		return response_data	


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

"""
# For Comic Table:

listOfComicFiles = open("data/allComics.txt")
COMICS_BASE_LINK = "data/comics/"

for eachComicFile in listOfComicFiles: 

	comicBook = {}

	filePath = COMICS_BASE_LINK+eachComicFile.strip()
	comicData = json.loads(open(filePath).read())

	comicBook["comic_id"] = comicData["id"]
	comicBook["title"] = comicData["title"]
	comicBook["description"] = comicData["description"] or "No description available"
	comicBook["image"] = comicData["thumbnail"]["path"]+"."+comicData["thumbnail"]["extension"]
	comicBook["details_url"] = "Missing Link"
	comicBook["purchase_url"] = "Missing Link"
	comicBook["price_digital"] = "Unavailable"
	comicBook["price_print"] = "Unavailable"

	for eachUrl in comicData["urls"]:
		if "detail" in eachUrl["type"]:
			comicBook["details_url"] = eachUrl["url"]
		if "purchase" in eachUrl["type"]:
			comicBook["purchase_url"] = eachUrl["url"]

	for eachUrl in comicData["prices"]:
		if "printPrice" in eachUrl["type"]:
			comicBook["price_digital"] = eachUrl["price"]
		if "digitalPurchasePrice" in eachUrl["type"]:
			comicBook["price_print"] = eachUrl["price"]
	
	newComic = Comic(
		comic_id = comicBook["comic_id"],
		title = comicBook["title"],
		description = comicBook["description"],
		image = comicBook["image"],
		details_url = comicBook["details_url"],
		purchase_url = comicBook["purchase_url"],
		price_digital = comicBook["price_digital"],
		price_print = comicBook["price_print"]
	);

	print comicBook["comic_id"]
	newComic.save()

"""
"""
#Add Aliases into Database
aliasesDict = json.loads(open("data/MarvelCharacters_Aliases.json").read())
for eachKey in aliasesDict:
	filteredChars = Character.objects.filter(name__icontains=aliasesDict[eachKey])
	if len(filteredChars)>0:
		character = filteredChars[0]
		if character.aliases == None or character.aliases == "":
			character.aliases = eachKey
		elif eachKey not in character.aliases:
			character.aliases += ", " + eachKey
		character.save()
"""


"""
#Add Detail URLs into Database
listOfCharsFiles = open("data/charactersList.txt")
CHAR_BASE_LINK = "data/characters/"

for eachCharFile in listOfCharsFiles: 
	filePath = CHAR_BASE_LINK+eachCharFile.strip()
	charData = json.loads(open(filePath).read())

	character = Character.objects.filter(character_id=charData["id"])[0]

	if "urls" in charData: 
		character.url = charData["urls"][0]["url"]
		character.save()

"""














