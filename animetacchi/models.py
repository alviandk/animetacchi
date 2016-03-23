#-*- encoding=UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_str, smart_unicode
from django.conf import settings
import os
import re
import json
from datetime import date, datetime, timedelta
from django.template.defaultfilters import slugify

from django.db.models import Q
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError
from service.tasks import send_notification
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from ratings.handlers import ratings
from ratings.forms import VoteForm

from vote.managers import VotableManager


class News(models.Model):
    news = models.TextField(null=True, blank=True)
    index_cover = models.ImageField(upload_to='IndexCover', null=True, blank=True)
    article = models.TextField(null=True, blank=True)
    seq_news = models.IntegerField(null=True,blank=True)

    def __unicode__(self):
        return unicode(self.news)


class Members(models.Model):
    user = models.ForeignKey(User)
    m_name = models.CharField(max_length=50, null=True)
    m_cover = models.ImageField(upload_to='MembersCover', null=True, blank=True)
    m_picture = models.ImageField(upload_to='MembersPicture', null=True, blank=True)
    m_bio = models.TextField(null=True, blank=True)
    m_tagline = models.CharField(max_length=50, null=True)
    blocked = models.BooleanField(default=False)
    seq_members = models.IntegerField(null=True)

    def __unicode__(self):
       return unicode(self.user.username)
'''
class Friendship(models.Model):
    user = models.ForeignKey(User)
    friend = models.ForeignKey(User, null=True, blank=True)
    seq_friendship = models.IntegerField(null=True)

    def __unicode__(self):
        return unicode(self.user.username)
'''
class About(models.Model):
    member = models.ForeignKey('Members', null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    seq_about = models.IntegerField(null=True)

    def __unicode__(self):
       return unicode(self.member)


class Genre(models.Model):
    genre_type = models.CharField(max_length=30, null=True )

    def __unicode__(self):
       return unicode(self.genre_type)


class Anime(models.Model):
    GENRE = (('Action', 'Action'), ('Adventure', 'Adventure'), ('Anime Influenced', 'Anime Influenced'), ('Comedy', 'Comedy'), ('Dementia', 'Dementia'), ('Demons', 'Demons'), ('Doujinshi', 'Doujinshi'), ('Drama', 'Drama'), ('Ecchi', 'Ecchi'), ('Fantasy', 'Fantasy'), ('Game', 'Game'), ('Gender Bender', 'Gender Bender'), ('Gore', 'Gore'), ('Harem', 'Harem'), ('Historical', 'Historical'), ('Horror', 'Horror'), ('Kids', 'Kids'), ('Magic', 'Magic'), ('Mahou Shoujo', 'Mahou Shoujo'), ('Mahou Shounen', 'Mahou Shounen'), ('Martial Arts', 'Martial Arts'), ('Mecha', 'Mecha'), ('Military', 'Military'), ('Music', 'Music'), ('Mystery', 'Mystery'), ('Parody', 'Parody'), ('Police', 'Police'), ('Psychological', 'Psychological'), ('Racing', 'Racing'), ('Romance', 'Romance'), ('Samurai', 'Samurai'), ('School', 'School'), ('Sci-Fi', 'Sci-Fi'), ('Shoujo Ai', 'Shoujo Ai'), ('Shounen Ai', 'Shounen Ai'), ('Slice of Life', 'Slice of Life'), ('Space', 'Space'), ('Sports', 'Sports'), ('Supernatural', 'Supernatural'), ('Super Power',  'Super Power'), ('Thriller', 'Thriller'), ('Vampire', 'Vampire'))

    a_name = models.CharField(max_length=50, null=True)
    a_genre = models.ManyToManyField(Genre)
    a_cover = models.ImageField(upload_to='AnimeCover', null=True, blank=True)
    a_displaypic = models.ImageField(upload_to='AnimePicture', null=True, blank=True)
    a_synopsys = models.TextField(null=True, blank=True)
    a_airedstart = models.DateField(null=True, blank=True)
    a_airedend = models.DateField(null=True, blank=True)
    save_added = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True)
    seq_anime = models.IntegerField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.a_name)
        super(Anime, self).save(*args, **kwargs)
    
    def __unicode__(self):
       return unicode(self.a_name)

class Manga(models.Model):
    GENRE = (('Action', 'Action'), ('Adventure', 'Adventure'), ('Anime Influenced', 'Anime Influenced'), ('Comedy', 'Comedy'), ('Dementia', 'Dementia'), ('Demons', 'Demons'), ('Doujinshi', 'Doujinshi'), ('Drama', 'Drama'), ('Ecchi', 'Ecchi'), ('Fantasy', 'Fantasy'), ('Game', 'Game'), ('Gender Bender', 'Gender Bender'), ('Gore', 'Gore'), ('Harem', 'Harem'), ('Historical', 'Historical'), ('Horror', 'Horror'), ('Kids', 'Kids'), ('Magic', 'Magic'), ('Mahou Shoujo', 'Mahou Shoujo'), ('Mahou Shounen', 'Mahou Shounen'), ('Martial Arts', 'Martial Arts'), ('Mecha', 'Mecha'), ('Military', 'Military'), ('Music', 'Music'), ('Mystery', 'Mystery'), ('Parody', 'Parody'), ('Police', 'Police'), ('Psychological', 'Psychological'), ('Racing', 'Racing'), ('Romance', 'Romance'), ('Samurai', 'Samurai'), ('School', 'School'), ('Sci-Fi', 'Sci-Fi'), ('Shoujo Ai', 'Shoujo Ai'), ('Shounen Ai', 'Shounen Ai'), ('Slice of Life', 'Slice of Life'), ('Space', 'Space'), ('Sports', 'Sports'), ('Supernatural', 'Supernatural'), ('Super Power',  'Super Power'), ('Thriller', 'Thriller'), ('Vampire', 'Vampire'))

    name = models.CharField(max_length=50, null=True)
    genre = models.ManyToManyField(Genre)
    cover = models.ImageField(upload_to='MangaCover', null=True, blank=True)
    displaypic = models.ImageField(upload_to='MangaPicture', null=True, blank=True)
    synopsys = models.TextField(null=True, blank=True)
    airedstart = models.DateField(null=True, blank=True)
    airedend = models.DateField(null=True, blank=True)
    save_added = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True)
    seq_manga = models.IntegerField(null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Manga, self).save(*args, **kwargs)
    
    def __unicode__(self):
       return unicode(self.name)


class WatchList(models.Model):
    STATUS = (('Bliss', 'Bliss'), ('Life', 'Life'),
	          ('Hope', 'Hope'), ('Agony', 'Agony'),)			
    members = models.ForeignKey('Members', null=True, blank=True)
    watchlist = models.ForeignKey('Anime', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, null=True)
    seq_watchlist = models.IntegerField(null=True)

    def __unicode__(self):
        return unicode(self.members)

class ReadingList(models.Model):
    STATUS = (('Bliss', 'Bliss'), ('Life', 'Life'),
	          ('Hope', 'Hope'), ('Agony', 'Agony'),)			
    members = models.ForeignKey('Members', null=True, blank=True)
    readinglist = models.ForeignKey('Manga', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, null=True)
    seq_watchlist = models.IntegerField(null=True)

    def __unicode__(self):
        return unicode(self.members)


class Character(models.Model):
    name = models.CharField(max_length=50, null=True)
    picture = models.ImageField(upload_to='CharacterPicture', null=True, blank=True)
    anime = models.ForeignKey('Anime', null=True, blank=True)    
    synopsys = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return (self.name)

class CharacterManga(models.Model):
    name = models.CharField(max_length=50, null=True)
    picture = models.ImageField(upload_to='CharacterPicture', null=True, blank=True)
    manga = models.ForeignKey('Manga', null=True, blank=True)        
    synopsys = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return (self.name)

class VoiceCharacter(models.Model):
    name = models.CharField(max_length=50, null=True)
    picture = models.ImageField(upload_to='VoiceActorPicture', null=True, blank=True)
    character = models.ManyToManyField('Character', null=True, blank=True)    
    synopsys = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return (self.name)


class Daisukilist(models.Model):
    members = models.ForeignKey('Members')
    anime = models.ManyToManyField(Anime,null=True, blank=True )
    manga = models.ManyToManyField(Manga,null=True, blank=True )
    character = models.ManyToManyField(Character,null=True, blank=True)    
    character_manga = models.ManyToManyField(CharacterManga,null=True, blank=True)
    voice_character = models.ManyToManyField(VoiceCharacter,null=True, blank=True)
	
    def __unicode__(self):
        return ('{}-daisuki'.format(self.members))

	
class Daikirailist(models.Model):
    members = models.ForeignKey('Members')
    anime = models.ManyToManyField(Anime,null=True, blank=True )
    manga = models.ManyToManyField(Manga,null=True, blank=True )
    character = models.ManyToManyField(Character,null=True, blank=True)
    character_manga = models.ManyToManyField(CharacterManga,null=True, blank=True)
		
    def __unicode__(self):
        return ('{}-daikirai'.format(self.members))

class Chart(models.Model):
    SEASON = (('winter', 'winter'), ('spring', 'spring'),
	          ('summer', 'summer'), ('fall', 'fall'),)			

    season = models.CharField(max_length=10, choices=SEASON, null=True)
    anime = models.ManyToManyField(Anime,null=True, blank=True )	
    year = models.IntegerField(null=True, blank=True)
	
    class Meta:
        ordering = ['year']
        
    def __unicode__(self):
        return ('{}-{}'.format(self.season, self.year))
       

class CommentAnime(models.Model):
    comment = models.TextField()
    user = models.ForeignKey('Members', null=True, blank=True)
    anime = models.ForeignKey('Anime', null=True, blank=True)
    added = models.DateTimeField(auto_now=True,null=True, blank=True)
    edited = models.DateTimeField(null=True, blank=True)
    votes = VotableManager()

    class Meta:
        ordering = ['-edited', '-added']
        
    def __unicode__(self):
        return ('{}-{}'.format(self.user, self.comment[:20]))

class CommentManga(models.Model):
    comment = models.TextField()
    user = models.ForeignKey('Members', null=True, blank=True)
    manga = models.ForeignKey('Manga', null=True, blank=True)
    added = models.DateTimeField(auto_now=True,null=True, blank=True)
    edited = models.DateTimeField(null=True, blank=True)
    votes = VotableManager()
    
    class Meta:
        ordering = ['-edited', '-added']    
        
    def __unicode__(self):
        return ('{}-{}'.format(self.user, self.comment[:20]))    


class UserProfile(models.Model):
    
    
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default= datetime.now)
      
    def __str__(self):
        return self.user.username

class RequestAnime(models.Model):
    content = models.TextField()
    user = models.ForeignKey('Members', null=True, blank=True)
    anime = models.ForeignKey('Anime', null=True, blank=True)
    added = models.DateTimeField(auto_now=True,null=True, blank=True)    
    

    class Meta:
        ordering = ['-added']
        
    def __unicode__(self):
        return ('{}-{}'.format(self.user, self.added))



ratings.register(Anime, score_range=(1, 5), form_class=VoteForm)
ratings.register(Manga, score_range=(1, 5), form_class=VoteForm)
ratings.register(Character, score_range=(1, 5), form_class=VoteForm)
ratings.register(CharacterManga, score_range=(1, 5), form_class=VoteForm)
ratings.register(VoiceCharacter, score_range=(1, 5), form_class=VoteForm)
