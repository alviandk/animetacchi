# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User, check_password
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, Template, RequestContext
from django.template.defaultfilters import slugify
from django.template import Template as template_django
from django.core import serializers
from django.core import urlresolvers
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.contrib import auth
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str, smart_unicode
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q, Count
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

import uuid
import simplejson



from datetime import date, datetime, timedelta, time


from animetacchi.models import *
from service.tasks import send_email_task, send_sms_task, send_notification

from restclient import POST

def email_send_with_api(subject, to, msg, fr=None):
	if not fr:
		fr = 'Animetacchi'
	url= 'http://www.tokowebku.com/api/email_sender/'
	form_fields = {'from': fr, 'subject': subject, 'to': to, 'msg': msg}
	result = POST(url, async=False, params=form_fields)
	return result

def home(request):
    #substract_date = datetime.now() - timedelta(days=3)
    #anime_data = Anime.objects.filter(save_added__gte=substract_date)
    anime_data = Anime.objects.all()[:3]
    index = News.objects.all()
    return render_to_response('index.html',locals(),context_instance=RequestContext(request))

def about(request):
    if request.POST.get('action') == 'saveAbout':
        aboutField = request.POST.get('about')
        memberField = request.POST.get('member')
        aboutData = About()
        aboutData.member = memberField
        aboutData.about = aboutField
        aboutData.save()
        return render_to_response('User/dashboard.html',locals(),context_instance=RequestContext(request))
    return render_to_response('about.html',locals(),context_instance=RequestContext(request))

def services(request):
    return render_to_response('services.html',locals(),context_instance=RequestContext(request))

def signin(request):
    if request.POST:
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            email = User.objects.get(email=email)
            cek_auth = auth.authenticate(username=email.username, password=password)
            auth.login(request, cek_auth)

        #Doesn't Exist
        except User.DoesNotExist:
            message_error = email +" does not exist, please register first."
            return render_to_response('signin.html', locals(), context_instance=RequestContext(request))

        #Not Match Email and Password
        except Exception, err:
            message_match = "The email and password that you entered don't match."
            return render_to_response('signin.html', locals(), context_instance=RequestContext(request))

        #Active User Filter
        members = Members.objects.get(user=request.user)
        if request.user.is_active is False:
            message_active = "Sorry, your ID is not active."
            return render_to_response('signin.html',locals(),context_instance=RequestContext(request))
        elif members.blocked is True:
            message_active = "Sorry, your ID is blocked."
            return render_to_response('signin.html',locals(),context_instance=RequestContext(request))

        message_success = 'success'
        member = Members.objects.get(user=request.user)
        return render_to_response('signin.html',locals(),context_instance=RequestContext(request))

    return render_to_response('signin.html',locals(),context_instance=RequestContext(request))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('home'))

def signup(request):
    if request.POST.get('action') == 'signup':
        username = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('passwd')
        if User.objects.filter(username=username):
            json_data = {'alert': 'Sorry, username ' + username + ' has been used!!', 'val': False}
            return HttpResponse(simplejson.dumps(json_data), content_type="application/json")
        if User.objects.filter(email=email):
            json_data = {'alert': 'Sorry, email ' + email + ' has been used!!', 'val': False}
            return HttpResponse(simplejson.dumps(json_data), content_type="application/json")
        usr = User.objects.create_user(username=username,email=email,password=password)
        usr.is_active = False # not active until he opens activation link
        usr.save()
        member = Members()
        member.user = usr
        member.m_name = username
        member.save()
        activation_key=str(uuid.uuid4())

        new_profile = UserProfile(user=usr, activation_key=activation_key)
        new_profile.save()
        host=request.META['HTTP_HOST']
        email_subject = 'Account confirmation'
        #email_body = "Hey {}, thanks for signing up. To activate your account, click this link within \
        #48 hours http://{}/confirm/{}".format(username, host, activation_key)
        send_mail(email_subject, email_body, 'be-py@alviandk.com',[email], fail_silently=False)
        email_send_with_api(email_subject, email, email_body, fr=None)
        json_data = {'alert': 'email_subject Success!!'}
        return HttpResponse(simplejson.dumps(json_data), content_type="application/json")
    return render_to_response('signup.html',locals(),context_instance=RequestContext(request))

def check_email(request):
    return render_to_response('User/check-email.html',locals(),context_instance=RequestContext(request))


def register_confirm(request, activation_key):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect(reverse('home'))

    # check if there is UserProfile which matches the activation key (if not then display 404)
    try:
        user_profile = UserProfile.objects.get(activation_key=activation_key)
    except:
        return HttpResponseRedirect(reverse('home'))

    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires + timedelta(days=1) < timezone.now():
        #user_profile.user.delete()
        return render_to_response('User/confirm_expired.html',locals(),context_instance=RequestContext(request))
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('User/confirm.html',locals(),context_instance=RequestContext(request))

def anime(request):
    #Search Function
    if request.POST.get('action') == 'search':
        search_val = request.POST.get('search_value')
        anime_data = Anime.objects.filter(a_name__contains=search_val).order_by('a_name')

        paginator = Paginator(anime_data, 10)
        try:
            page = int(request.GET.get('page'))
            if not page:
                page = 1
        except Exception:
            page = 1

        anime_data = paginator.page(page).object_list
        current_page = paginator.page(page)
        number = current_page.number

        if request.GET.get('pages_ajax') is not None :
            pass

        return render_to_response('anime_data.html',locals(),context_instance=RequestContext(request))

    #Sorting Function
    if request.POST.get('action') == 'checkbox':
        anime_check = json.loads(request.POST.get('anime_check'))
        if len(anime_check) > 0:
            anime_data = Anime.objects.filter(a_genre__in=anime_check)#.distinct('a_name')
        else:
            anime_data = Anime.objects.all().order_by('a_name')

        paginator = Paginator(anime_data, 10)
        try:
            page = int(request.GET.get('page'))
            if not page:
                page = 1
        except Exception:
            page = 1

        anime_data = paginator.page(page).object_list
        current_page = paginator.page(page)
        number = current_page.number

        if request.GET.get('pages_ajax') is not None :
            pass

        return render_to_response('anime_data.html',locals(),context_instance=RequestContext(request))

    #Default Data
    genre = Genre.objects.all()
    anime_data = Anime.objects.all().order_by('a_name')
    paginator = Paginator(anime_data, 10)
    try:
        page = int(request.GET.get('page'))
        if not page:
            page = 1
    except Exception:
        page = 1

    anime_data = paginator.page(page).object_list
    current_page = paginator.page(page)
    number = current_page.number

    if request.GET.get('pages_ajax') is not None :
        return render_to_response('anime_data.html', locals(), context_instance=RequestContext(request))

    return render_to_response('anime.html',locals(),context_instance=RequestContext(request))

def manga(request):
    #Search Function
    if request.POST.get('action') == 'search':
        search_val = request.POST.get('search_value')
        manga_data = Manga.objects.filter(name__contains=search_val).order_by('name')

        paginator = Paginator(manga_data, 10)
        try:
            page = int(request.GET.get('page'))
            if not page:
                page = 1
        except Exception:
            page = 1

        manga_data = paginator.page(page).object_list
        current_page = paginator.page(page)
        number = current_page.number

        if request.GET.get('pages_ajax') is not None :
            pass

        return render_to_response('manga_data.html',locals(),context_instance=RequestContext(request))

    #Sorting Function
    if request.POST.get('action') == 'checkbox':
        manga_check = json.loads(request.POST.get('manga_check'))
        if len(manga_check) > 0:
            manga_data = Manga.objects.filter(genre__in=manga_check)#.distinct('name')
        else:
            manga_data = Manga.objects.all().order_by('name')

        paginator = Paginator(manga_data, 10)
        try:
            page = int(request.GET.get('page'))
            if not page:
                page = 1
        except Exception:
            page = 1

        manga_data = paginator.page(page).object_list
        current_page = paginator.page(page)
        number = current_page.number

        if request.GET.get('pages_ajax') is not None :
            pass

        return render_to_response('manga_data.html',locals(),context_instance=RequestContext(request))

    #Default Data
    genre = Genre.objects.all()
    manga_data = Manga.objects.all().order_by('name')
    paginator = Paginator(manga_data, 10)
    try:
        page = int(request.GET.get('page'))
        if not page:
            page = 1
    except Exception:
        page = 1

    manga_data = paginator.page(page).object_list
    current_page = paginator.page(page)
    number = current_page.number

    if request.GET.get('pages_ajax') is not None :
        return render_to_response('manga_data.html', locals(), context_instance=RequestContext(request))

    return render_to_response('manga.html',locals(),context_instance=RequestContext(request))

def anime_details(request,slug):
    anime_data = Anime.objects.get(slug=slug)
    commentanimes = CommentAnime.objects.filter(anime=anime_data).annotate(likes=Count('votes')).order_by('-likes','-edited','-added')

    #c.votes.up(request.user)
    try:
		members = Members.objects.get(user=request.user)
    except:
        pass
    try:
        Daisukilist.objects.get(anime=anime_data, members=members)
        daisuki = True
    except:
        daisuki = False
    try:

        Daikirailist.objects.get(anime=anime_data, members=members)
        daikirai = True
    except:
        daikirai = False
    try:
        watchlist=WatchList.objects.get(members=members, watchlist=anime_data)
    except:
        watchlist = False
    return render_to_response('anime_details.html',locals(),context_instance=RequestContext(request))

def manga_details(request,slug):
    manga_data = Manga.objects.get(slug=slug)
    commentmangas = CommentManga.objects.filter(manga=manga_data).annotate(likes=Count('votes')).order_by('-likes','-edited','-added')
    try:
		members = Members.objects.get(user=request.user)
    except:
        pass
    try:
        Daisukilist.objects.get(manga=manga_data, members=members)
        daisuki = True
    except:
        daisuki = False
    try:

        Daikirailist.objects.get(manga=manga_data, members=members)
        daikirai = True
    except:
        daikirai = False
    try:
        watchlist=ReadingList.objects.get(members=members, readinglist=manga_data)
    except:
        watchlist = False

    return render_to_response('manga_details.html',locals(),context_instance=RequestContext(request))


def anime_character(request,slug,id):
    anime = Anime.objects.get(slug=slug)
    character = Character.objects.get(id=id)
    try:
		members = Members.objects.get(user=request.user)
    except:
        pass
    try:
        Daisukilist.objects.get(character=character, members=members)
        daisuki = True
    except:
        daisuki = False
    try:
        Daikirailist.objects.get(character=character, members=members)
        daikirai = True
    except:
        daikirai = False

    return render_to_response('anime_character.html',locals(),context_instance=RequestContext(request))

def manga_character(request,slug,id):
    manga = Manga.objects.get(slug=slug)
    character = CharacterManga.objects.get(id=id)
    try:
		members = Members.objects.get(user=request.user)
    except:
        pass
    try:
        Daisukilist.objects.get(character_manga=character, members=members)
        daisuki = True
    except:
        daisuki = False
    try:
        Daikirailist.objects.get(character_manga=character, members=members)
        daikirai = True
    except:
        daikirai = False

    return render_to_response('manga_character.html',locals(),context_instance=RequestContext(request))

def anime_voice(request,id):

    voice = VoiceCharacter.objects.get(id=id)
    try:
		members = Members.objects.get(user=request.user)
    except:
        pass
    try:
        Daisukilist.objects.get(voice_character=voice, members=members)
        daisuki = True
    except:
        daisuki = False
    return render_to_response('anime_voice.html',locals(),context_instance=RequestContext(request))

def anime_reviews(request,slug):
    anime_data = Anime.objects.get(slug=slug)
    try:
		member = Members.objects.get(user=request.user)
    except:
		pass
    commentanimes = CommentAnime.objects.filter(anime=anime_data).annotate(likes=Count('votes')).order_by('-likes','-edited','-added')


    return render_to_response('anime_reviews.html',locals(),context_instance=RequestContext(request))

@login_required
def anime_reviews_add(request,slug):
    anime_data = Anime.objects.get(slug=slug)
    member = Members.objects.get(user=request.user)


    if request.method == "POST":
		comment=CommentAnime.objects.create(comment=request.POST.get('comment'), user=member, anime=anime_data)
		comment.save()
		return HttpResponseRedirect(reverse('anime_reviews',kwargs={'slug':anime_data.slug}))

    return render_to_response('anime_reviews_add.html',locals(),context_instance=RequestContext(request))


def manga_reviews(request,slug):
    manga_data = Manga.objects.get(slug=slug)
    try:
		member = Members.objects.get(user=request.user)
    except:
		pass
    commentmangas = CommentManga.objects.filter(manga=manga_data).annotate(likes=Count('votes')).order_by('-likes','-edited','-added')



    return render_to_response('manga_reviews.html',locals(),context_instance=RequestContext(request))


@login_required
def manga_reviews_add(request,slug):
    manga_data = Manga.objects.get(slug=slug)
    member = Members.objects.get(user=request.user)


    if request.method == "POST":
		comment=CommentManga.objects.create(comment=request.POST.get('comment'), user=member, manga=manga_data)
		comment.save()
		return HttpResponseRedirect(reverse('manga_reviews',kwargs={'slug':manga_data.slug}))

    #return render_to_response('manga_reviews_add.html',locals(),context_instance=RequestContext(request))


def anime_chart(request,season):
    try:
        anime_data = Chart.objects.get(season=season)
    except:
	    anime_data =[]
    return render_to_response('anime_chart.html',locals(),context_instance=RequestContext(request))


def users(request,username):
    if request.user.username == username:
        return HttpResponseRedirect(reverse('dashboard', kwargs={'username': username}))
    try:
        user = User.objects.get(username=username)
    except:
        return HttpResponseRedirect(reverse('home'))
    member = Members.objects.get(user=user)
    return render_to_response('User/dashboard.html',locals(),context_instance=RequestContext(request))


def dashboard(request, username):
    if request.POST.get('action') == 'saveAbout':
        countData = About.objects.all().count()
        aboutField = request.POST.get('about')
        seq_about = request.POST.get('seq_about')
        memberId = request.POST.get('member')
        member = Members.objects.get(id=memberId)
        aboutData = About()
        if seq_about is not None:
            aboutData = About.objects.get(seq_about=seq_about)
            aboutData.member = member
            aboutData.about = aboutField
            aboutData.seq_about = seq_about
            aboutData.save()
            return render_to_response('User/dashboard.html',locals(),context_instance=RequestContext(request))
        aboutData.member = member
        aboutData.about = aboutField
        aboutData.seq_about = countData
        aboutData.save()
        return render_to_response('User/dashboard.html',locals(),context_instance=RequestContext(request))

    if request.user.is_authenticated():
        member = Members.objects.get(user=request.user)
        usr = User.objects.get(username=username)
        if request.user.username != username:
            return HttpResponseRedirect(reverse('users', kwargs={'username': username}))
        about_data = About.objects.filter(member=member.id)
        return render_to_response('User/dashboard.html',locals(),context_instance=RequestContext(request))
    return HttpResponseRedirect(reverse('home'))

def library(request,username):



        usr = User.objects.get(username=username)
        member = Members.objects.get(user=usr)
        bliss = WatchList.objects.filter(members=member,status='Bliss')
        agony = WatchList.objects.filter(members=member,status='Agony')
        hope = WatchList.objects.filter(members=member,status='Hope')
        life = WatchList.objects.filter(members=member,status='Life')
        host=request.META['HTTP_HOST']
        about_data = About.objects.filter(member=member.id)
        return render_to_response('User/library.html',locals(),context_instance=RequestContext(request))


def library_manga(request,username):



        usr = User.objects.get(username=username)
        member = Members.objects.get(user=usr)
        bliss = ReadingList.objects.filter(members=member,status='Bliss')
        agony = ReadingList.objects.filter(members=member,status='Agony')
        hope = ReadingList.objects.filter(members=member,status='Hope')
        life = ReadingList.objects.filter(members=member,status='Life')
        host=request.META['HTTP_HOST']

        about_data = About.objects.filter(member=member.id)
        return render_to_response('User/library-manga.html',locals(),context_instance=RequestContext(request))



def daikirai(request):
    #Search Function

    if request.method=="POST":

        username = request.POST.get('username')
        user = User.objects.get(username=username)
        members = Members.objects.get(user=user)

        try:
            daikirai = Daikirailist.objects.get(members=members)
        except:
            daikirai = Daikirailist.objects.create(members=members)
        try:
            daisuki = Daisukilist.objects.get(members=members)
        except:
            daisuki = Daisukilist.objects.create(members=members)

        if request.POST.get('anime_id'):
			anime_id = request.POST.get('anime_id')
			anime = Anime.objects.get(id=int(anime_id))
			daikirai.anime.add(anime)
			daisuki.anime.remove(anime)
        elif request.POST.get('manga_id'):
            manga_id = request.POST.get('manga_id')
            manga = Manga.objects.get(id=int(manga_id))
            daikirai.manga.add(manga)
            daisuki.manga.remove(manga)
        elif request.POST.get('character_id'):
            character_id = request.POST.get('character_id')
            character = Character.objects.get(id=int(character_id))
            daikirai.character.add(character)
            daisuki.character.remove(character)
        elif request.POST.get('character_manga_id'):
            character_manga_id = request.POST.get('character_manga_id')
            character_manga = CharacterManga.objects.get(id=int(character_manga_id))
            daikirai.character_manga.add(character_manga)
            daisuki.character_manga.remove(character_manga)

        daikirai.save()
        daisuki.save()


        return HttpResponse("success")

def daisuki(request):
    #Search Function

    if request.method=="POST":

        username = request.POST.get('username')
        user = User.objects.get(username=username)
        members = Members.objects.get(user=user)

        try:
            daikirai = Daikirailist.objects.get(members=members)
        except:
            daikirai = Daikirailist.objects.create(members=members)
        try:
            daisuki = Daisukilist.objects.get(members=members)
        except:
            daisuki = Daisukilist.objects.create(members=members)

        if request.POST.get('anime_id'):
			anime_id = request.POST.get('anime_id')
			anime = Anime.objects.get(id=int(anime_id))
			daisuki.anime.add(anime)
			daikirai.anime.remove(anime)
        elif request.POST.get('manga_id'):
            manga_id = request.POST.get('manga_id')
            manga = Manga.objects.get(id=int(manga_id))
            daisuki.manga.add(manga)
            daikirai.manga.remove(manga)
        elif request.POST.get('character_id'):
            character_id = request.POST.get('character_id')
            character = Character.objects.get(id=int(character_id))
            daisuki.character.add(character)
            daikirai.character.remove(character)
        elif request.POST.get('character_manga_id'):
            character_manga_id = request.POST.get('character_manga_id')
            character_manga = CharacterManga.objects.get(id=int(character_manga_id))
            daisuki.character_manga.add(character_manga)
            daikirai.character_manga.remove(character_manga)
        elif request.POST.get('voice_id'):
            voice_id = request.POST.get('voice_id')
            voice = VoiceCharacter.objects.get(id=int(voice_id))
            daisuki.voice_character.add(voice)


        daikirai.save()
        daisuki.save()


        return HttpResponse("success")

def watchlist(request):
    #Search Function

    if request.method=="POST":

        username = request.POST.get('username')
        user = User.objects.get(username=username)
        members = Members.objects.get(user=user)
        anime_id = request.POST.get('anime_id')
        anime = Anime.objects.get(id=int(anime_id))

        try:
            watchlist = WatchList.objects.get(members=members,watchlist=anime)
        except:
            watchlist = WatchList.objects.create(members=members,watchlist=anime)

        watchlist.status=request.POST.get('status')

        watchlist.save()

        return HttpResponse("success")

def readinglist(request):
    #Search Function

    if request.method=="POST":

        username = request.POST.get('username')
        user = User.objects.get(username=username)
        members = Members.objects.get(user=user)
        manga_id = request.POST.get('manga_id')
        manga = Manga.objects.get(id=int(manga_id))

        try:
            readinglist = ReadingList.objects.get(members=members,readinglist=manga)
        except:
            readinglist = ReadingList.objects.create(members=members, readinglist=manga)

        readinglist.status=request.POST.get('status')

        readinglist.save()

        return HttpResponse("success")

def ratings_average(request, entity, id):

    if entity == 'anime':
        entities = Anime.objects.get(id=int(id))
    elif entity == 'manga':
        entities = Manga.objects.get(id=int(id))
    elif entity == 'character':
        entities = Character.objects.get(id=int(id))
    elif entity == 'character_manga':
        entities = CharacterManga.objects.get(id=int(id))
    elif entity == 'voice':
        entities = VoiceCharacter.objects.get(id=int(id))

    return render_to_response('ratings_average.html',locals(),context_instance=RequestContext(request))

def likes(request, entity):

    if request.method=="POST":
        username = request.POST.get('username')
        id = request.POST.get('id')
        user = User.objects.get(username=username)
        members = Members.objects.get(user=user)
        if entity == 'anime':
            try:
                entities = CommentAnime.objects.get(id=int(id))
            except:
                entities = CommentAnime.objects.create(id=int(id))
        elif entity == 'manga':
            try:
                entities = CommentManga.objects.get(id=int(id))
            except:
                entities = CommentManga.objects.create(id=int(id))

        voted = entities.votes.exists(user)
        if voted:
            entities.votes.down(user)
        else:
            entities.votes.up(user)
        voted = entities.votes.exists(user)
        total_votes = entities.votes.count()

        json_data = {'voted': voted, 'total_votes': total_votes}

        return HttpResponse(simplejson.dumps(json_data), content_type="application/json")

def show_likes(request, entity, id):

    username = request.user
    user = User.objects.get(username=username)
    members = Members.objects.get(user=user)
    print user
    if entity == 'anime':
        entities = CommentAnime.objects.get(id=int(id))

    elif entity == 'manga':
        entities = CommentManga.objects.get(id=int(id))

    voted = entities.votes.exists(user)

    json_data = {'voted': voted}

    return HttpResponse(simplejson.dumps(json_data), content_type="application/json")


def sort_comment(request):


    if request.method=="POST":

        by = request.POST.get('by')
        anime_id = request.POST.get('anime_id')
        anime_data = Anime.objects.get(id=int(anime_id))

        if by == 'likes':
            commentanimes = CommentAnime.objects.filter(anime=anime_data).annotate(likes=Count('votes')).order_by('-likes','-edited','-added')
        elif by == 'time':
			commentanimes = CommentAnime.objects.filter(anime=anime_data).order_by('-edited','-added')

        return render_to_response('sort-comment.html',locals(),context_instance=RequestContext(request))

def sort_comment_manga(request):


    if request.method=="POST":

        by = request.POST.get('by')
        manga_id = request.POST.get('manga_id')
        manga_data = Manga.objects.get(id=int(manga_id))

        if by == 'likes':
            commentmangas = CommentManga.objects.filter(manga=manga_data).annotate(likes=Count('votes')).order_by('-likes','-edited','-added')
        elif by == 'time':
			commentmangas = CommentManga.objects.filter(manga=manga_data).order_by('edited','added')

        return render_to_response('sort-comment-manga.html',locals(),context_instance=RequestContext(request))

def search_comment(request):

    if request.method=="POST":

        if request.POST.get('anime_id'):
			anime_id = request.POST.get('anime_id')
			search_val = request.POST.get('search')
			anime_data = Anime.objects.get(id=int(anime_id))
			commentanimes = CommentAnime.objects.filter(anime=anime_data, comment__icontains=search_val).order_by('-edited','-added')
			if not commentanimes:
				return HttpResponse("<h4>Sorry no data</h4>")
			return render_to_response('sort-comment.html',locals(),context_instance=RequestContext(request))
        elif request.POST.get('manga_id'):
			manga_id = request.POST.get('manga_id')
			search_val = request.POST.get('search')
			manga_data = Manga.objects.get(id=int(manga_id))
			commentmangas = CommentManga.objects.filter(manga=manga_data, comment__icontains=search_val).order_by('-edited','-added')
			if not commentmangas:
				return HttpResponse("<h4>Sorry no data</h4>")
			return render_to_response('sort-comment-manga.html',locals(),context_instance=RequestContext(request))


def request_edit(request):

    if request.method=="POST":

        if request.POST.get('anime_id'):
			anime_id = request.POST.get('anime_id')
			synopsis = request.POST.get('synopsis')
			start = request.POST.get('synopsis')
			end = request.POST.get('end')
			content = "synopsis: {} \nstart: {} \nend: {}".format(synopsis, start, end)
			anime = Anime.objects.get(id=int(anime_id))
			username = request.POST.get('username')
			user = User.objects.get(username=username)
			members = Members.objects.get(user=user)
			requestedit= RequestAnime.objects.create(content=content, user=members, anime=anime)
			requestedit.save()
			return render_to_response('sort-comment.html',locals(),context_instance=RequestContext(request))

