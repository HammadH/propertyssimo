from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
import settings
from listings import views as listing_views
import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.Landing.as_view(), name='home'),
    url(r'^buying/$', views.Buyers.as_view(), name='buyers'),
    url(r'^selling/$', views.Selling.as_view(), name='selling'),
    url(r'^properties/$', 'listings.views.show_listings', name='show_listings'),
    url(r'^property/(?P<id>\d+)$', 'listings.views.listing_details', name='listing_details'),
    url(r'^properties/create/$', csrf_exempt(listing_views.Platform.as_view()), name='create_listing'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))


if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()