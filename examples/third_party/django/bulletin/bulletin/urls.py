from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from simpleauth.views import SimpleAuthRegistrationView
from django.contrib.auth import views as auth_views

# CHANGEME: Must include the view class.
from notes.views import NoteCreate

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bulletin.views.home', name='home'),
    # url(r'^bulletin/', include('bulletin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^register/$', SimpleAuthRegistrationView.as_view(), name='registration_register'),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='auth_logout'),

    url(r'^$', 'notes.views.index', name='home'),

    # CHANGEME: allow logged in users to add notes.
    url(r'^add/$', NoteCreate.as_view(), name='add_note'),
)
