"""EntrySystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from entrycontrol import views as entrycontrol_views
from eventcenter import views as eventcenter_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^EntryControl/$', entrycontrol_views.here, name= 'entrycontrol'),
    url(r'^EntryControl/EntryPolicy', entrycontrol_views.entrypolicy, name= 'entrypolicy'),
    url(r'^EntryControl/UserData', entrycontrol_views.getuser, name= 'getuser'),
    url(r'^EntryControl/Group/$', entrycontrol_views.getgroup, name= 'getgroup'),
    url(r'^EntryControl/Group/(?P<GroupName>(\w.+))/$', entrycontrol_views.group_member, name='group_member'),  
    url(r'^EventCenter/EventView', eventcenter_views.currenteventview, name= 'currenteventView'),  
    url(r'^EventCenter/EventSearch', eventcenter_views.eventsearch, name= 'eventsearch'),
    url(r'^ReaderView/$', eventcenter_views.readersview, name= 'readersview'),
    url(r'^ReaderView/(?P<FQDN>(\w.+))/$', eventcenter_views.readerview, name= 'readerview'),
]
