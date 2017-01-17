"""online_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.auth.views import login

from . import views

app_name = 'library'
urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', views.LibraryView.as_view(), name='index'),
    url(r'^login$', login, {'template_name' : 'library/login.html'}, name='login'),
    url(r'^logout$', views.log_out, name='logout'),
    url(r'^register$', views.Registration.as_view(), name='register'),

    url(r'^upload$', views.BookEdit.as_view(), name='upload'),
    url(r'^(?P<book_id>[0-9A-Za-z]+)/$', views.BookView.as_view(), name='book_view'),
    url(r'^edit/(?P<book_id>[0-9A-Za-z]+)$', views.BookEdit.as_view(), name='book_edit'),
    #url(r'^(?P<book_id>[0-9A-Za-z]+)/(?P<book_page>([1-9][0-9*]))/$', views.BookRead.as_view(), name='read'),

    #url(r'^user/edit/(?P<user_name>[0-9A-Za-z]+)$', views.UserEdit.as_view(), name='edit_user'),
    #url(r'^user/(?P<user_name>[0-9A-Za-z]+)$', views.UserView.as_view(), name='view_user')
]
