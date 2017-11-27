# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from entrycontrol.models import group, domain, userdata, doorsecurity, readerdata, p_list
from django.views.decorators.csrf import csrf_exempt 
from django.utils import timezone
import os, time, datetime

from cassandra.cluster import Cluster 


Policymsgs = []


def here(request):
	userdatas = userdata.objects.using('entry_system').all()
	string = 'i am here!'
	return render_to_response('here.html',{'userdatas':userdatas})

@csrf_exempt
def entrypolicy(request):
	Groups = group.objects.values_list('group_name')
	Userdatas = userdata.objects.values_list('userid')
	Domains = domain.objects.values_list('domain_name')
	Doors = readerdata.objects.filter(inout='1')

	Policylists=[]
	Messages = []
	Day = 0
	Group = ''
	Domain = ''
	StartDate = ''
	EndDate = ''
	StartTime =''
	EndTime =''
	

	if 'Confirm' in request.POST :
		policyformat = True
		PolicyRole = request.POST['policyrole']
		if request.POST['group'] !='None':
			Group = request.POST['group']
		else:
			policyformat = False
			Messages.append('Group must enroll\n')

		if request.POST['domain'] !='None':
			Domain = request.POST['domain']
		else:
			policyformat = False
			Messages.append('Domain must enroll\n')
		


		if request.POST['Startdate'] !='':
			StartDate = str(request.POST['Startdate'])
			StartDate = StartDate.split('-')[0]+StartDate.split('-')[1]+StartDate.split('-')[2]
		else:
			policyformat = False
			Messages.append('Start Date must enroll\n')

		if request.POST['Enddate'] !='':
			EndDate = str(request.POST['Enddate'])
			EndDate = EndDate.split('-')[0]+EndDate.split('-')[1]+EndDate.split('-')[2]
		else:
			Messages.append('End Date must enroll\n')
			policyformat = False
		if 'mon' in request.POST:
			Day = Day + 1
			mon = True
		if 'tue' in request.POST:
			Day = Day + 2
			tue = True
		if 'wes' in request.POST:
			Day = Day + 4
			wes = True
		if 'thu' in request.POST:
			Day = Day + 8
			thu = True
		if 'fri' in request.POST:
			Day = Day + 16
			fri = True
		if 'sat' in request.POST:
			Day = Day + 32
			sat = True
		if 'sun' in request.POST:
			Day = Day + 64
			sun = True
		if Day == 0:
			Messages.append('Work Day must enroll\n')
			policyformat = False


		if request.POST['Starttime'] !='':
			if int(request.POST['Starttime']) <= 9:
				StartTime = "0"+str(request.POST['Starttime'])
			else:	 
				StartTime = str(request.POST['Starttime'])
			StartTime = StartTime + "00"
		else:
			Messages.append('Start Time must enroll\n')
			policyformat = False

		if request.POST['Endtime'] !='':
			if int(request.POST['Endtime']) <= 9:
				EndTime = "0"+str(request.POST['Endtime'])
			else:	 
				EndTime = str(request.POST['Endtime'])
			EndTime = EndTime + "00"
		else:
			Messages.append('End Time must enroll\n')
			policyformat = False

		# if Day == 0:
		if policyformat == True:
			Policymsg = 'policy '+PolicyRole+' -I '+Group+' -D '+Domain+' -T '+StartDate+' '+EndDate+' '+str(Day)+' '+StartTime+' '+EndTime
			Messages.append(Policymsg)
			Policymsgs.append(Policymsg+'\n')
			# Policymsgs = []
	
		print PolicyRole, Group, Domain, StartDate, EndDate, Day, StartTime, EndTime, policyformat
		doorsecuritys = doorsecurity.objects.all()
	if 'Apply' in request.POST :
		applied = False
		policyconfig = open(os.path.join('policylist.conf'), 'a')
		for Policy in Policymsgs:
			if len(Policy) !=0:
				policyconfig.write(Policy)
				applied = True
		if applied ==True:
			Messages.append('Policy apply\n')
		else:
			Messages.append('Policy apply Fail, policy command is empty\n')
		del Policymsgs[:]

	# print policylists
	try:
		policyconfig = open(os.path.join('policylist.conf'), 'r')
		policyconfig_lines = policyconfig.readlines()
		for i in range(1,len(policyconfig_lines)):
			Policylists.append(policyconfig_lines[i].split('\n')[0]+'\n')

	except IOError:
		policyconfig = open(os.path.join('policylist.conf'), 'w')
		policyconfig.write('policy list config\n')
		print 'Create policylist.conf file'

	return render_to_response('entrypolicy.html',{'Groups':Groups, 'Userdatas':Userdatas,'Messages':Messages,'Domains':Domains,'Doors':Doors,'Policymsgs':Policymsgs,'PolicyLists':Policylists})

@csrf_exempt
def getuser(request):
	users = userdata.objects.all()
	last_user_id = 1
	if 'Confirm' in request.POST :
		uid = request.POST['userid']
		psw = request.POST['psw']
		lstname = request.POST['lstname']
		fstname = request.POST['fstname']
		try:
			manager = request.POST['manager']
		except:
			print "False"
			manager = False
		else:
			print "True"
			manager = True
		try:
			if_user_null = userdata.objects.all()
		except:
			last_user_id = 1
		else:
			for userlast in users:
				last_user_id = userlast.id + 1
				

		userdata.objects.create(
			qid=1,
			id=last_user_id, 
			userid=uid,
			createtime=timezone.localtime(timezone.now()),
			modifytime=timezone.localtime(timezone.now()),
			firstname=fstname, 
			lastname=lstname,
			password=psw,
			manager=manager)
	

	#users = userdata.objects.order_by('-id')
	return render_to_response('user.html', {'users':users})

@csrf_exempt
def getgroup(request):
	groups = group.objects.all()
	last_group_id = 1
	if 'Confirm' in request.POST:
		try:
			if_columns_null = group.objects.all()
		except:
			print "NONODATA"
			last_group_id = 1
		else:
			print "UES"
			for getlast in groups:
				last_group_id = getlast.group_id + 1

		name = request.POST['group_name']
		member=[]
		member.append('ADMIN')
		description = request.POST['group_description']
		group.objects.create(
			qid=1,
			group_id=last_group_id, 
			create_time=timezone.localtime(timezone.now()),
			group_name=name, 
			group_member=list(member),
			group_description=description)



	return render_to_response('group.html', {'groups':groups})
	# return render_to_response('group.html', {'groups':groups, 'last_group_id':last_group_id})

@csrf_exempt
def group_member(request, GroupName):
	Group = group.objects.allow_filtering().get(group_name = GroupName)
	groupid = Group.group_id
	if 'Confirm' in request.POST:
		selectedusers = request.POST.getlist('objectSelect')
		# print selectedusers
		group.objects.filter(qid=1,group_name = GroupName,group_id=groupid).update(group_member=list(selectedusers), modify_time=timezone.localtime(timezone.now()))
	groups = group.objects.allow_filtering().get(group_name = GroupName)
	users = userdata.objects.all()
	alluser_list = []
	for user in users:
		# print user.userid
		alluser_list.append(user.userid)
	group_users = []
	group_users = groups.group_member
	# print user_list
	# print alluser_list
	s1 = set(alluser_list)
	s2 = set(group_users)
	# print s1.difference(s2)
	available_users = list(s1.difference(s2))
	return render_to_response('group_member.html', {'groups':Group, 'group_users':group_users, 'available_users':available_users})

@csrf_exempt
def getdomain(request):
	domains = domain.objects.all()
	last_domain_id = 1
	if 'Confirm' in request.POST:
		try:
			if_columns_null = domain.objects.all()
		except:
			last_domain_id = 1
		else:
			for getlast in domains:
				last_domain_id = getlast.domain_id + 1

		name = request.POST['domain_name']
		member=[]
		member.append('ADMIN')
		description = request.POST['domain_description']
		domain.objects.create(
			qid=1,
			domain_id=last_domain_id, 
			create_time=timezone.localtime(timezone.now()),
			domain_name=name, 
			domain_member=list(member),
			domain_description=description)

	return render_to_response('domain.html', {'domains':domains})


@csrf_exempt
def domain_reader(request, DomainName):
	Domain = domain.objects.allow_filtering().get(group_name = GroupName)
	domainid = Domain.group_id
	if 'Confirm' in request.POST:
		selectedusers = request.POST.getlist('objectSelect')
		# print selectedusers
		domain.objects.filter(qid=1,domain_name = GroupName,domain_id=domainid).update(domain_member=list(selectedusers), modify_time=timezone.localtime(timezone.now()))
	groups = group.objects.allow_filtering().get(group_name = GroupName)
	users = userdata.objects.all()
	alluser_list = []
	for user in users:
		# print user.userid
		alluser_list.append(user.userid)
	group_users = []
	group_users = groups.group_member
	# print user_list
	# print alluser_list
	s1 = set(alluser_list)
	s2 = set(group_users)
	# print s1.difference(s2)
	available_users = list(s1.difference(s2))
	return render_to_response('group_member.html', {'groups':Group, 'group_users':group_users, 'available_users':available_users})


