from django.conf.urls import include, url

from django.contrib import admin
from django.contrib.auth import views as auth_views
admin.autodiscover()

import crank.views

urlpatterns = [
    url(r'^$', crank.views.index, name='index'),
    url(r'^db', crank.views.db, name='db'),
    url(r'^login/$', auth_views.login, {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page':'/'}, name='logout'),
    url(r'^signup/$', crank.views.signup, name='signUp'),
    url(r'^delete', crank.views.delete, name='delete'),
    url(r'^users', crank.views.users, name='users'),
    url(r'^admin/', include(admin.site.urls)),
]
