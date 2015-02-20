from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings

import views

urlpatterns = patterns('',
    # Examples:
     url(r'^$', views.Landing.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

)

if settings.DEBUG == True:
	urlpatterns += staticfiles_urlpatterns()

