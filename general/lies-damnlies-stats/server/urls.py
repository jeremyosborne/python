from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # authentication
    url(r'^api/auth/info', 'auth.views.auth_info'),
    url(r'^api/auth/login', 'auth.views.auth_login'),
    url(r'^api/auth/logout', 'auth.views.auth_logout'),

    # stats
    url(r'^api/stats/delete', 'stats.views.delete'),
    url(r'^api/stats/describe', 'stats.views.describe'),
    url(r'^api/stats/get', 'stats.views.get'),
    url(r'^api/stats/save', 'stats.views.save'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
