from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import auth
from twitter.models import *
from twitter.forms import CustomUserCreationForm
from django.contrib.auth import logout
import datetime

try:
    import cPickle as pickle
except ImportError:
    import pickle


# Create your views here.

TWEETS_EN_PAGE = 5			#La cantidad de tweets que se muestran por p�gina
TWEETS_EN_PROFILE = 10		#La cantidad de tweets que se muestran en prefiles

# Create your views here.
def index(request, page = 1):
    if int(page) < 2:
        page = 1
    n = TWEETS_EN_PAGE * (int(page) - 1)
    tweets_ = Tweet.objects.filter(activo=True).order_by('-fecha')[n:n + TWEETS_EN_PAGE]
    tweets = []
    for t in tweets_:
        t.profile = Profile.objects.get(user_id=t.user_id)
        tweets.append(t)

    if request.user.is_authenticated():
        ntweets = len(Tweet.objects.filter(user=request.user, activo=True))
        return render_to_response('twitter/index.html',
                                  {'logueado': request.user,
                                   'p': Profile.objects.get(user=request.user),
                                   'next': int(page) + 1,
                                   'page': page,
                                   'prev': int(page) - 1,
                                   'tweets': tweets,
                                   'ntweets': ntweets,
                                   'exito': '0'},
                                  RequestContext(request))
    else:
        form = CustomUserCreationForm()
        return render_to_response('twitter/login.html',
                                  {'next': int(page) + 1,
                                   'page': page,
                                   'prev': int(page) - 1,
                                   'tweets': tweets,
                                   'form': form,
                                   'exito': '0'},
                                  RequestContext(request))


def twitter_login(request,page = 1):
    if page < 2:
        page = 1
    n = TWEETS_EN_PAGE * (int(page) - 1)
    tweets_ = Tweet.objects.filter(activo=True).order_by('-fecha')[n:n + TWEETS_EN_PAGE]
    tweets = []
    for t in tweets_:
        t.profile = Profile.objects.get(user_id=t.user_id)
        tweets.append(t)

    form = CustomUserCreationForm()
    return render_to_response('twitter/login.html',	{'exito': '0',
                                                        'next': int(page) + 1,
                                                        'page': page,
                                                        'prev': int(page) - 1,
                                                        'tweets': tweets,
                                                        'form': form},	RequestContext(request))

def register(request,page = 1):
    try:
        #####################################################333
        try:
            if request.method == 'POST':
                form = CustomUserCreationForm(request.POST)
                if form.is_valid():
                    form.save()
                    username = request.POST.get('email', '')
                    password = request.POST.get('password1', '')
                    user = auth.authenticate(username=username, password=password)
                    if user is not None:
                        p = Profile.objects.create(
                            user=user,
                            frase='',
                            ubicacion='',
                            avatar=''
                        )
                        p.save()
                        auth.login(request, user)

                        if page < 2:
                            page = 1
                        n = TWEETS_EN_PAGE * (int(page) - 1)
                        tweets_ = Tweet.objects.filter(activo=True).order_by('-fecha')[n:n + TWEETS_EN_PAGE]
                        tweets = []
                        for t in tweets_:
                            t.profile = Profile.objects.get(user_id=t.user_id)
                            tweets.append(t)

                        return render_to_response(
                            'twitter/login.html',
                            {'mensaje_register': 'Registrado correctamente, Loguese!',
                             'next': int(page) + 1,
                             'page': page,
                             'prev': int(page) - 1,
                             'tweets': tweets,
                             'exito': '1'},
                            RequestContext(request))
                    else:
                        return render_to_response('twitter/login.html',
                                                  {'mensaje_register': 'Error en el registro del usuario',
                                                    'exito': '0'},
                                                  RequestContext(request))
                else:
                    return render_to_response('twitter/login.html',
                                              {'mensaje_register': 'Error en el registro del formulario',
                                                'exito': '0',
                                                'form': form},
                                              RequestContext(request))
            else:
                form = CustomUserCreationForm()
                return render_to_response('twitter/login.html',
                                          {'mensaje_register': 'Error en el registro del envio',
                                            'exito': '0','form': form},
                                              RequestContext(request))
        except KeyError:
            form = CustomUserCreationForm()
            return render_to_response('twitter/login.html',
                                      {'mensaje_register': 'Error en el registro general',
                                       'exito': '0','form': form},
                                      RequestContext(request))
            #####################################################333
    except KeyError:
        form = CustomUserCreationForm()
        return render_to_response('twitter/login.html',
                                  {'mensaje_register': 'Error en el registro general',
                                   'exito': '0','form': form}, RequestContext(request))

def login_process(request, page = 1):
    try:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
    except KeyError:
        return render_to_response('twitter/login.html', {
            'mensaje_login': 'Rellene todos los campos',
        }, RequestContext(request))

    if page < 2:
        page = 1
    n = TWEETS_EN_PAGE * (int(page) - 1)
    tweets_ = Tweet.objects.filter(activo=True).order_by('-fecha')[n:n + TWEETS_EN_PAGE]
    tweets = []
    for t in tweets_:
        t.profile = Profile.objects.get(user_id=t.user_id)
        tweets.append(t)


    user = auth.authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            auth.login(request, user)
        else:
            return render_to_response('twitter/login.html', {
                'mensaje_login': 'El usuario ha sido eliminado',
                'next': int(page) + 1,
                'page': page,
                'prev': int(page) - 1,
                'tweets': tweets,
            }, RequestContext(request))
    else:
        return render_to_response('twitter/login.html', {
            'mensaje_login': 'Ingrese el usuario y clave correctamente',
            'next': int(page) + 1,
            'page': page,
            'prev': int(page) - 1,
            'tweets': tweets,
        }, RequestContext(request))
    return HttpResponseRedirect(reverse('twitter_inicio'))


def twitter_logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('twitter_inicio'))


def tweet(request):
    try:
        content = request.POST['content']
    except KeyError:
        return HttpResponseRedirect(reverse('twitter_inicio'))
    try:
        respuesta = int(request.POST['respuesta'])
    except (KeyError, ValueError):
        respuesta = None

    if respuesta is None:
        t = Tweet.objects.create(
            user=request.user,
            fecha=datetime.datetime.now(),
            contenido=content,
        )
    else:
        t = Tweet.objects.create(
            user=request.user,
            fecha=datetime.datetime.now(),
            contenido=content,
            respuesta=respuesta,
        )
    t.save()
    return HttpResponseRedirect(reverse('twitter_inicio'))


def conf(request):
    u = request.user
    p = get_object_or_404(Profile, user = u)
    #p = Profile.get_profile(u.id)
    try:
        if request.POST['procesa'] == 'profile':
            u.first_name = request.POST['firstname']
            u.last_name = request.POST['lastname']
            u.save()

            p.ubicacion = request.POST['ubicacion']
            p.frase = request.POST['bio']
            #p.avatar = request.POST['avatar']
            p.logo = request.FILES['logo']
            p.save()
        elif request.POST['procesa'] == 'pass':
            if not u.check_password(request.POST['oldpass']):
                return render_to_response('twitter/conf.html', {
                    'mensaje': '<h3>Introduzca su contraseña actual correctamente</h3>',
                    'nombre': u.first_name,
                    'apellido': u.last_name,
                    'email': u.email,
                    'ubicacion': p.ubicacion,
                    'bio': p.frase,
                    'logo': p.logo,
                    'logueado': request.user,
                    'ntweets': len(Tweet.objects.filter(user=request.user, activo=True)),
                    'p': Profile.objects.get(user=request.user),
                }, RequestContext(request))

            if request.POST['pass'] == request.POST['pass2']:
                u.set_password(request.POST['pass'])
                u.save()
                logout(request)
                return HttpResponseRedirect(reverse('twitter_inicio'))
            else:
                return render_to_response('twitter/conf.html',{
                    'mensaje' : 'Las contraseñas no coinciden',
                    'p' : Profile.objects.get(user = request.user),
                    'nombre' : u.first_name,
                    'apellido' : u.last_name,
                    'email' : u.email,
                    'ubicacion' : p.ubicacion,
                    'bio' : p.frase,
                    'logo': p.logo,
                    'logueado' : request.user,
                    'ntweets' : len(Tweet.objects.filter(user = request.user, activo = True)),
                    }, RequestContext(request))
        return HttpResponseRedirect(reverse('twitter_config'))
    except KeyError:
        return render_to_response('twitter/conf.html',{
            'p' : Profile.objects.get(user = request.user),
            'nombre' : u.first_name,
            'apellido' : u.last_name,
            'email' : u.email,
            'ubicacion' : p.ubicacion,
            'bio' : p.frase,
            'avatar' : p.avatar,
            'logo': p.logo,
            'logueado' : request.user,
            'ntweets' : len(Tweet.objects.filter(user = request.user, activo = True)),
            }, RequestContext(request))



def borrar(request, tweet_id):
	t = get_object_or_404(Tweet, id = tweet_id)
	if t.user == request.user or request.user.is_staff: #El usuario actual es el propietario del tweeet
		t.activo = False
		t.save()
	return HttpResponseRedirect(reverse('twitter_inicio'))

def profile(request, page = 1):
	if page < 2:
		page = 1
	n = TWEETS_EN_PROFILE * (int(page) - 1)
	u = request.user
	p = Profile.objects.get(user = request.user) #El perfil del usuario

	#Procesa retweets
	tweets_ = u.tweet_set.all().filter(activo = True).order_by('-fecha')
	tweets = []
	for t in tweets_:
		t.profile = Profile.objects.get(user = t.user)
		tweets.append(t)

	return render_to_response('twitter/profile.html',
	{
		'length' : len(tweets),
		'logueado' : request.user,
		'p' : Profile.objects.get(user = request.user),
		'next' : int(page) + 1,
		'page' : page,
		'prev' : int(page) - 1,
		'profile' : get_object_or_404(Profile, user=u),
		'tweets' : tweets[n:n + TWEETS_EN_PROFILE],
		'user' : u,
		'ntweets' : len(Tweet.objects.filter(user = request.user, activo = True)),
	}, RequestContext(request))
