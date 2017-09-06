from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Album,Song
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.views import generic
from oauth2_provider.views.generic import ProtectedResourceView

from social_django.models import UserSocialAuth

#http://localhost:8000/oauth/complete/github/



#
# def index(request):
#     all_albums = Album.objects.all()
#     html = ''
#     for album in all_albums:
#         url='/myapp/'+str(album.id)+'/'
#         html +='<a href="'+url+' ">'+album.album_title+'</a> <br>'
#     return HttpResponse(html)
#
# def index(request):
#     all_albums = Album.objects.all()
#     template = loader.get_template('myapp/index.html')
#     context = {'all_albums': all_albums, }
#     return HttpResponse(template.render(context, request))
# class ApiEndpoint(ProtectedResourceView):
#     def get(self, request, *args, **kwargs):
#         return HttpResponse('Hello, OAuth2!')



def index(request):
    all_albums=Album.objects.all()
    context ={'all_albums': all_albums}
    return render(request,'myapp/index.html',context)



def hello(request):
    text = """ <h1> Hello request </h1>"""
    return HttpResponse(text)

#
# def details(request, album_id):
#     try:
#         album=Album.objects.get(pk=album_id)
#     except Album.DoesNotExist:
#         raise Http404("Album doesnot exist")
#
#     return render(request, 'myapp/details.html', {'album':album})


def details(request, album_id):
    #album=Album.objects.get(pk=album_id)
    album=get_object_or_404(Album, pk=album_id)
    return render(request, 'myapp/details.html', {'album':album})
    #return HttpResponse("<h2> Album id is : " + str(album_id)+" </h2> ")


def favorite(request, album_id):
    album=get_object_or_404(Album, pk=album_id)
    try:
        selected_song=album.song_set.get(pk=request.POST['song'])
    except (KeyError, Song.DoesNotExist):




        return render(request, 'myapp/detail.html',{
        'album': album,
        'error_message': "You didnot select a valid song"

    })
    else:
        selected_song.is_favorite= True
        selected_song.save()
        return render(request, 'myapp/detail.html', {'album': album})
# Create your views here.

# class UserFormView(View):
#     form_class = UserForm
#     template_name='myapp/register.html'
# #display blank form
#     def get(self, request):
#         form=self.form_class(None)
#         return render(request, self.template_name, {'form':form})
# # process form data
#     def post(self, request):
#         form =self.form_class(request.POST)
#         #template_name ='myapp/welcome'
#         if form.is_valid():
#             user=form.save(commit=False)
#
#             #cleaned data
#
#             Username = form.cleaned_data['Username']
#             Password = form.cleaned_data['Password']
#             user.set_password(Password)
#             user.save()
#
#             # returns User Objects if credentials are correct
#
#             user=authenticate(Username=Username,Password=Password)
#             if user is not None:
#                 if user.is_active:
#                     login(request,user)
#                     return redirect('myapp:register')
#
#         return render(request, self.template_name, {'form':form})

#@login_required
def login(request):
    return render(request, 'myapp/login.html')

def welcome(request):
      return render(request,'myapp/welcome.html')



def qis(request):
#
#     form=UserForm(request.POST or None)
#     if form.is_valid():
#         user = form.save(commit=False)
#         Username  = form.cleaned_data['Username']
#         Password = form.cleaned_data['Password']
#         user.set_password(Password)
#         user.save()
#         user=authenticate(Username=Username,Password=Password)
    return render(request, 'myapp/qis.html', {'messgae':'User login in '})

def lms(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = UserForm()


    return render(request, 'myapp/lms.html', {'form':form})


def lmsextend(request):

    return render(request,'myapp/lmsextend.html')

# @login_required
# def settings(request):
#     user = request.user
#
#     try:
#         github_login = user.social_auth.get(provider='github')
#     except UserSocialAuth.DoesNotExist:
#         github_login = None
#     try:
#         twitter_login = user.social_auth.get(provider='twitter')
#     except UserSocialAuth.DoesNotExist:
#         twitter_login = None
#     try:
#         google_login = user.social_auth.get(provider='google')
#     except UserSocialAuth.DoesNotExist:
#         google_login = None
#
#     can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
#
#     return render(request, 'myapp/settings.html', {
#         'github_login': github_login,
#         'twitter_login': twitter_login,
#         'google_login': google_login,
#         'can_disconnect': can_disconnect
#     })