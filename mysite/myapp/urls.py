from django.conf.urls import url, include
from . import views
import oauth2_provider.views as oauth2_views
from django.conf import settings
#from .views import ApiEndpoint

app_name ='myapp'














urlpatterns = [
    url(r'^index/', views.index, name='index'),
    #url(r'^hello/', views.hello, name='hello'),
    #url(r'^lms/',views.lms, name='lms'),
    url(r'^qis/',views.qis, name='qis'),
    #url(r'^login/',views.login, name='login'),
    #url(r'^settings/$',views.settings, name='settings'),
    url(r'welcome/',views.welcome, name='welcome'),
    url(r'^lms/',views.lms,name='lms'),
    #url(r'register/',views.UserFormView.as_view(), name='register'),
    #/myapp/1
   # url(r'^(?P<album_id>[0-9]+)/$', views.details, name='details'),
#/myapp/album_id/favorite
    #url(r'^(?P<album_id>[0-9]+)/favorite$', views.favorite, name='favorite'),
  ]

# Create your views here.
