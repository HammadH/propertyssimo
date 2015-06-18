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
    url(r'^buying/$', views.Buyers.as_view(), name='buying'),
     url(r'^careers/$', views.Careers.as_view(), name='careers'),
    url(r'^about-us/$', views.AboutUs.as_view(), name='about_us'),
     url(r'^services/$', views.Services.as_view(), name='services'),
    url(r'^investing/$', views.Investing.as_view(), name='investing'),
    url(r'^renter/$', views.Renter.as_view(), name='renter'),
     url(r'^vacations/$', views.Vacation.as_view(), name='vacation'),
    url(r'^selling/$', views.Selling.as_view(), name='selling'),
     url(r'^landlords/$', views.Landlords.as_view(), name='landlords'),
    url(r'^dubai_marina/$', views.Marina.as_view(), name='marina'),
    url(r'^jbr/$', views.JBR.as_view(), name='jbr'),
    url(r'^palm/$', views.Palm.as_view(), name='palm'),
    url(r'^downtown/$', views.Downtown.as_view(), name='downtown'),
    url(r'^site_listings/$', views.SiteListings.as_view(), name='site_listings'),
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