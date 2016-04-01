from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'animetacchi.views.home', name='home'),
    url(r'^about/$', 'animetacchi.views.about', name='about'),
    url(r'^services/$', 'animetacchi.views.services', name='services'),
    
    # account
    url(r'^logout/$', 'animetacchi.views.logout', name='logout'),
    url(r'^signin/$', 'animetacchi.views.signin', name='signin'),
    url(r'^signup/$', 'animetacchi.views.signup', name='signup'),
    url(r'^confirm/(?P<activation_key>[a-zA-Z\-\_0-9\: ]+)/$', 'animetacchi.views.register_confirm', name='confirm'),
    url(r'^check-email/$', 'animetacchi.views.check_email', name='check_email'),
    
    # chart
    url(r'^chart/(?P<season>[a-zA-Z\-\_0-9]+)/$', 'animetacchi.views.anime_chart', name='anime_chart'),
    
    # anime
    url(r'^anime/$', 'animetacchi.views.anime', name='anime'),    
    url(r'^anime/(?P<slug>[a-zA-Z\-\_0-9\: ]+)/$', 'animetacchi.views.anime_details', name='anime_details'),
    url(r'^anime/(?P<slug>[a-zA-Z\-\_0-9\: ]+)/reviews/$', 'animetacchi.views.anime_reviews', name='anime_reviews'),
    url(r'^anime/(?P<slug>[a-zA-Z\-\_0-9\: ]+)/reviews/add/$', 'animetacchi.views.anime_reviews_add', name='anime_reviews_add'),
    url(r'^anime/(?P<slug>[a-zA-Z\-\_0-9\: ]+)/character/(?P<id>\d+)/$', 'animetacchi.views.anime_character', name='anime_character'),
    url(r'^anime/voice/(?P<id>\d+)/$', 'animetacchi.views.anime_voice', name='anime_voice'),
    
    url(r'^daikirai/$', 'animetacchi.views.daikirai', name='daikirai'),
    url(r'^daisuki/$', 'animetacchi.views.daisuki', name='daisuki'),
    url(r'^watchlist/$', 'animetacchi.views.watchlist', name='watchlist'),
    url(r'^readinglist/$', 'animetacchi.views.readinglist', name='readinglist'),
    
    
    
    # manga
    url(r'^manga/$', 'animetacchi.views.manga', name='manga'),
    url(r'^manga/(?P<slug>[a-zA-Z\-\_0-9\: ]+)/$', 'animetacchi.views.manga_details', name='manga_details'),    
    url(r'^manga/(?P<slug>[a-zA-Z\-\_0-9\: ]+)/reviews/$', 'animetacchi.views.manga_reviews', name='manga_reviews'),
    url(r'^manga/(?P<slug>[a-zA-Z\-\_0-9\: ]+)/reviews/add/$', 'animetacchi.views.manga_reviews_add', name='manga_reviews_add'),
    url(r'^manga/(?P<slug>[a-zA-Z\-\_0-9\: ]+)/character/(?P<id>\d+)/$', 'animetacchi.views.manga_character', name='manga_character'),
    
    # user
    url(r'^dashboard/(?P<username>[-\w.]+)/$', 'animetacchi.views.dashboard', name='dashboard'),
    url(r'^users/(?P<username>[-\w.]+)/$', 'animetacchi.views.users', name='users'),
    url(r'^users/(?P<username>[-\w.]+)/library/$', 'animetacchi.views.library', name='library'),    
    url(r'^users/(?P<username>[-\w.]+)/library/manga/$', 'animetacchi.views.library_manga', name='library_manga'),
    url(r'^forgot-password/$', 'animetacchi.views.forgot_password', name='forgot-password'),
    url(r'^password_reset/done/$', 'animetacchi.views.cust_password_reset_done'),
    url(r'^reset/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$', 'animetacchi.views.cust_password_reset_confirm'),
    url(r'^reset/done/$', 'animetacchi.views.cust_password_reset_complete'),


    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    #ratings
    url(r'^ratings/', include('ratings.urls')),
    url(r'^ratings/average/(?P<entity>[a-zA-Z\-\_0-9\: ]+)/(?P<id>[a-zA-Z\-\_0-9\: ]+)/', 'animetacchi.views.ratings_average', name='ratings_average'),
    
    #likes
    url(r'^likes/(?P<entity>[a-zA-Z\-\_0-9\: ]+)/', 'animetacchi.views.likes', name='likes'),
    url(r'^show_likes/(?P<entity>[a-zA-Z\-\_0-9\: ]+)/(?P<id>[a-zA-Z\-\_0-9\: ]+)/', 'animetacchi.views.show_likes', name='show_likes'),
    
    url(r'^sort_comment/$', 'animetacchi.views.sort_comment', name='sort_comment'),
    url(r'^sort_comment_manga/$', 'animetacchi.views.sort_comment_manga', name='sort_comment_manga'),
    
    url(r'^search_comment/$', 'animetacchi.views.search_comment', name='search_comment'),
    
    url(r'^request_edit/$', 'animetacchi.views.request_edit', name='request_edit'),

)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)
