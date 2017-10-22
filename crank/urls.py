from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from django.contrib import admin
from django.contrib.auth import views as auth_views
admin.autodiscover()

import crank.views

urlpatterns = [
    url(r'^$', crank.views.index, name='index'),
    url(r'^db', crank.views.db, name='db'),
    url(r'^login/$', auth_views.login, {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page':'/'}, name='logout'),
    url(r'^accounts/login/$', auth_views.login, {'template_name':'login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page':'/'}, name='logout'),
    url(r'^signup/$', crank.views.signup, name='signUp'),
    url(r'^account_activation_sent/$', crank.views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        crank.views.activate, name='activate'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^delete', crank.views.delete, name='delete'),
    url(r'^users', crank.views.users, name='users'),
    url(r'^admin/', include(admin.site.urls)),
]
