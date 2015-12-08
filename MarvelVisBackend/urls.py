"""MarvelVisBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from manager import CharacterManager, FilterManager


urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),

    # CharacterManager API Calls
	# url(r'^api/character/$', CharacterManager.charRequest, name='charrequest'),
	# url(r'^api/character/(?P<character_id>\d*)/$', CharacterManager.charRequest, name='chardata'),

    # For Filters
    url(r'^api/filter/all/$', FilterManager.filterAll, name='filter_all'),     

    url(r'^api/filter/affiliation/$', FilterManager.affiliationRequest, name='affiliations_all'), 
    url(r'^api/filter/nationality/$', FilterManager.nationalityRequest, name='nationality_all'), 
    url(r'^api/filter/year_introduced/$', FilterManager.yearIntroducedRequest, name='year_introduced_all'), 
    url(r'^api/filter/gender/$', FilterManager.genderRequest, name='gender_all'),     
    url(r'^api/filter/appearances/$', FilterManager.appearancesRange, name='appearances_all'), 

    # For Connection URLs
    url(r'^api/connections/$', FilterManager.connectionsForChar, name='connections_char'), 

    # Get Detailed Character
    url(r'^api/character/$', FilterManager.getDetailedCharacter, name='detailed_character'), 

    url(r'^api/comic/random/$', FilterManager.getCommonRandomComic, name='random_common_comic'),     


    # For Setting Character Attributes
    # url(r'^api/gender/set/$', CharacterManager.setGenders, name='set_genders'), 
    # url(r'^api/affiliation/set/$', CharacterManager.setAffiliation, name='set_affiliations'), 
    # url(r'^api/relations/set/$', CharacterManager.setRelations, name='set_relations'), 
    # url(r'^api/relations/setConnectionCounts/$', CharacterManager.setConnectionCounts, name='set_connectionCounts'), 
    # url(r'^api/comic_characters/set/$', CharacterManager.setComicChars, name='set_comicChars'), 
    # url(r'^api/comic_connections/set/$', CharacterManager.setComicConnections, name='set_comicChars'), 

]
