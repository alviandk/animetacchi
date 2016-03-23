from animetacchi.models import *
from django.contrib import admin
from django import forms

class NewsAdmin(admin.ModelAdmin):
    list_display = ['news','index_cover','article']
    search_fields = ['news']

class MembersAdmin(admin.ModelAdmin):
    list_display = ['user', 'm_name', 'm_cover', 'm_picture', 'm_bio', 'm_tagline', 'seq_members']
    search_fields = ['m_name', 'm_tagline']

class GenresAdmin(admin.ModelAdmin):
    list_display = ['genre_type']
    search_fields = ['genre_type']


class AnimeAdmin(admin.ModelAdmin):
    list_display = ['a_name', 'a_displaypic', 'a_synopsys', 'a_airedstart', 'a_airedend']
    search_fields = ['a_name', 'a_displaypic', 'a_synopsys', 'a_airedstart', 'a_airedend']

#et-projectsAdmin
admin.site.register(News, NewsAdmin)
admin.site.register(Members, MembersAdmin)
#admin.site.register(Friendship)
admin.site.register(Genre, GenresAdmin)
admin.site.register(About)
admin.site.register(Character)
admin.site.register(VoiceCharacter)
admin.site.register(Anime, AnimeAdmin)
admin.site.register(WatchList)
admin.site.register(Daisukilist)
admin.site.register(Daikirailist)
admin.site.register(CommentAnime)
admin.site.register(Chart)

admin.site.register(Manga)
admin.site.register(ReadingList)
admin.site.register(CharacterManga)
admin.site.register(CommentManga)

admin.site.register(UserProfile)
admin.site.register(RequestAnime)
