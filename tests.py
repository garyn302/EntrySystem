# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, sys
sys.path.append("/home/user/EntrySystem/EntrySystem")
os.environ["DJANGO_SETTINGS_MODULE"] = "EntrySystem.settings"
from django.test import TestCase
from entrycontrol.models import group, domain, userdata, doorsecurity, readerdata, p_list
# Create your tests here.
Policylists = []
policyconfig = open(os.path.join('policylist.conf'), 'r')
policyconfig_lines = policyconfig.readlines()
for i in range(1,len(policyconfig_lines)):
	policy = policyconfig_lines[i].split('\n')[0]
	print policy.split(' ')[1]


