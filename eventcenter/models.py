# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class event(models.Model):
    insert_time = models.TextField()
    event_name = models.TextField()
    reader_fqdn = models.TextField()
    reader_id = models.TextField()
    reader_ip = models.TextField()
    door_name = models.TextField(null=True)
    event_level = models.IntegerField()    
    event_type = models.IntegerField()
    description = models.TextField(null=True)
    
    def __unicode__(self):
        return self.reader_fqdn


class readermib(models.Model):
    insert_time = models.TextField(null=True)
    reader_fqdn = models.TextField(primary_key=True)
    reader_ip = models.TextField()
    reader_id = models.TextField(null=True)
    reader_role = models.TextField(null=True)
    reader_status = models.TextField(null=True)
    cassandra = models.NullBooleanField()
    postgresql = models.NullBooleanField()
    rfid = models.NullBooleanField()
    finger_vein = models.NullBooleanField()
    door_status = models.NullBooleanField()
    door_open_timer = models.IntegerField(null=True)
    identify_fail = models.IntegerField(null=True)
    account_fail = models.IntegerField(null=True)
    rfid_fail = models.IntegerField(null=True)
    finger_fail = models.IntegerField(null=True)
    competence = models.IntegerField(null=True)
    competence_fail = models.IntegerField(null=True)
    policy_fail = models.IntegerField(null=True)
    apb_fail = models.IntegerField(null=True)
    manager_check_fail = models.IntegerField(null=True)
    os = models.TextField(null=True)


class eventrole(models.Model):
    event_level = models.IntegerField()
    event_level_name = models.TextField()
    event_name = models.TextField(null=True)
    event_type = models.IntegerField(null=True)
    event_type_description = models.TextField(null=True)
    event_enable = models.BooleanField()
    event_threshold = models.IntegerField(null = True)
    event_threshold_level = models.IntegerField(null = True)

class eventlevel(models.Model):
    event_level = models.IntegerField(primary_key=True)
    event_level_name = models.TextField()
    event_name = models.TextField(null=True)


