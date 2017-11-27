# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


# Create your models here.  DjangoCassandraModel

class group(Model):
	group_id = columns.Integer(primary_key=True)
	create_time = columns.DateTime()
	modify_time = columns.DateTime()
	group_name = columns.Text(index = True)
	group_member = columns.List(columns.Text)
	group_description = columns.Text()

class domain(Model):
	domain_id = columns.Integer(primary_key=True)
	create_time = columns.DateTime()
	modify_time = columns.DateTime()
	domain_name = columns.Text()
	domain_member = columns.Text()
	domain_description = columns.Text()

class userdata(Model):
	id = columns.Integer(index = True)
	userid = columns.Text(primary_key=True)
	createtime = columns.DateTime()
	modifytime = columns.DateTime()
	firstname = columns.Text()
	lastname = columns.Text()
	password = columns.Text()
	manager = columns.Boolean()
	rfid = columns.Text(index = True)
	group = columns.Text()
	update_flag = columns.Integer(index = True)

class doorsecurity(Model):
	id = columns.Integer(primary_key=True)
	createtime = columns.DateTime()
	modifytime = columns.DateTime()
	enable = columns.Boolean()
	group = columns.Text(index = True)
	domain = columns.Text(index = True)
	start_date = columns.Date()
	end_date = columns.Date()
	work_day = columns.Text()
	begin_time = columns.Text()
	end_time = columns.Text()

class p_list(Model):
	id = columns.Integer(primary_key=True)
	domain = columns.Text()
	createtime = columns.DateTime()
	modifytime = columns.DateTime()
	userid = columns.Text()
	userid_finger = columns.Text()
	partiton = columns.Text(index = True)

class readerdata(Model):
	fqdn = columns.Text(primary_key=True)
	registertime = columns.DateTime()
	offtime = columns.DateTime()
	id = columns.Text()
	role = columns.Text()
	ip = columns.Text()
	areaid = columns.Text()
	inout = columns.Text(index = True)
	door = columns.Text()
	doorname = columns.Text()
	domain = columns.Text()
	status = columns.Text(index = True)

class fingerdata(Model):
	createtime = columns.DateTime()
	modifytime = columns.DateTime()
	userid = columns.Text(primary_key=True)
	fid = columns.Text()
	fingerdata = columns.Blob()
	fingerdata_length = columns.Integer()
