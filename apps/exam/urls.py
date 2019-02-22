from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index),
    url(r'^register$',views.register),
    url(r'^login$',views.login),
    #
    url(r'^dashboard$',views.dashboard),
    #
    url(r'^logout$',views.logout),

    url(r'^trips/new$',views.newtrip),
    url(r'^trips/new/process$',views.trips_new_process),
 
    url(r'^trips/edit/(?P<trip_edit_id>[0-9]+)$',views.edit_trip),
    url(r'^edit/process/(?P<edit_id>[0-9]+)$',views.edit_process),

    url(r'^trips/(?P<trip_show_id>[0-9]+)$',views.show_trip_info),

    url(r'^cancel/(?P<cancelid>[0-9]+)$',views.cancel),
 
    url(r'^remove/(?P<removeid>[0-9]+)$',views.remove),
    url(r'^join/(?P<joinid>[0-9]+)$',views.join_trip),

    ]