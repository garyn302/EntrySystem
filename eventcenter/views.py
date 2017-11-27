# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt 
from eventcenter.models import event, readermib
from datetime import datetime, date, time


# Create your views here.
def currenteventview(request):
	events = event.objects.order_by('-id')[:10]#依順序排列，取最新前10筆資料
	return render_to_response('currenteventview.html',{'events':events})

@csrf_exempt
def eventsearch(request):
	Readers = readermib.objects.order_by('reader_fqdn')
	if request.POST :
		Date = True
		Time = True
		ReaderFQDN = request.POST['readerfqdn']
		if request.POST['Startdate'] !='':
			StartDate = str(request.POST['Startdate'])
		else:
			Date = False
		if request.POST['Starttime'] !='':
			if int(request.POST['Starttime']) <= 9:
				StartTime = "0"+str(request.POST['Starttime'])
			else:	 
				StartTime = str(request.POST['Starttime'])
		else:
			Time = False

		if Date == True and Time == True:
			TIME = StartDate+" "+StartTime#+":00:00"
			events = event.objects.filter(reader_fqdn= ReaderFQDN,insert_time__contains = TIME).order_by('id')#,insert_time__iexact = search
			print TIME, ReaderFQDN
		else:
			events = event.objects.filter(reader_fqdn = ReaderFQDN).order_by('-id')[:15]#.order_by('-id')[:5]#filter(reader_fqdn = '1.1.101.1.2')依順序排列，取最新前5筆資料

		# print str(events)
		return render_to_response('eventsearch.html',{'events':events,'Readers':Readers})#
	else:
		return render_to_response('eventsearch.html',{'Readers':Readers})


def readersview(request):
	Readers = readermib.objects.order_by('reader_fqdn')
	
	return render_to_response('readersview.html',{'Readers':Readers})

def readerview(request, FQDN):
	Reader = readermib.objects.get(reader_fqdn = FQDN)
	return render_to_response('readerview.html',{'Reader':Reader})
