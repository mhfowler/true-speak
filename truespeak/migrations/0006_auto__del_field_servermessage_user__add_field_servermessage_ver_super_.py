# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ServerMessage.user'
        db.delete_column(u'truespeak_servermessage', 'user_id')

        # Adding field 'ServerMessage.ver_super'
        db.add_column(u'truespeak_servermessage', 'ver_super',
                      self.gf('django.db.models.fields.CharField')(default='0.0', max_length=100),
                      keep_default=False)

        # Adding field 'ServerMessage.ver_sub'
        db.add_column(u'truespeak_servermessage', 'ver_sub',
                      self.gf('django.db.models.fields.CharField')(default='0', max_length=100),
                      keep_default=False)

        # Deleting field 'UserProfile.last_message_execution'
        db.delete_column(u'truespeak_userprofile', 'last_message_execution')

        # Adding field 'UserProfile.last_message'
        db.add_column(u'truespeak_userprofile', 'last_message',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ServerMessage.user'
        raise RuntimeError("Cannot reverse this migration. 'ServerMessage.user' and its values cannot be restored.")
        # Deleting field 'ServerMessage.ver_super'
        db.delete_column(u'truespeak_servermessage', 'ver_super')

        # Deleting field 'ServerMessage.ver_sub'
        db.delete_column(u'truespeak_servermessage', 'ver_sub')


        # User chose to not deal with backwards NULL issues for 'UserProfile.last_message_execution'
        raise RuntimeError("Cannot reverse this migration. 'UserProfile.last_message_execution' and its values cannot be restored.")
        # Deleting field 'UserProfile.last_message'
        db.delete_column(u'truespeak_userprofile', 'last_message')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'truespeak.emailprofile': {
            'Meta': {'object_name': 'EmailProfile'},
            'confirmation_link': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'truespeak.prikey': {
            'Meta': {'object_name': 'PriKey'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pri_key_text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'truespeak.pubkey': {
            'Meta': {'object_name': 'PubKey'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_key_text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'truespeak.servermessage': {
            'Meta': {'object_name': 'ServerMessage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ver_sub': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '100'}),
            'ver_super': ('django.db.models.fields.CharField', [], {'default': "'0.0'", 'max_length': '100'})
        },
        u'truespeak.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_message': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['truespeak']