# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Facebook_User'
        db.create_table(u'truespeak_facebook_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fb_id', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=400, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=400, null=True)),
        ))
        db.send_create_signal(u'truespeak', ['Facebook_User'])

        # Adding model 'UserProfile'
        db.create_table(u'truespeak_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('facebook_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['truespeak.Facebook_User'], unique=True, null=True, blank=True)),
            ('pubkeys', self.gf('django.db.models.fields.TextField')(default='[]')),
            ('plugin_token', self.gf('django.db.models.fields.CharField')(max_length=400)),
        ))
        db.send_create_signal(u'truespeak', ['UserProfile'])

        # Adding M2M table for field friends on 'UserProfile'
        db.create_table(u'truespeak_userprofile_friends', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'truespeak.userprofile'], null=False)),
            ('facebook_user', models.ForeignKey(orm[u'truespeak.facebook_user'], null=False))
        ))
        db.create_unique(u'truespeak_userprofile_friends', ['userprofile_id', 'facebook_user_id'])


    def backwards(self, orm):
        # Deleting model 'Facebook_User'
        db.delete_table(u'truespeak_facebook_user')

        # Deleting model 'UserProfile'
        db.delete_table(u'truespeak_userprofile')

        # Removing M2M table for field friends on 'UserProfile'
        db.delete_table('truespeak_userprofile_friends')


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
        u'truespeak.facebook_user': {
            'Meta': {'object_name': 'Facebook_User'},
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True'})
        },
        u'truespeak.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'facebook_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['truespeak.Facebook_User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'+'", 'null': 'True', 'to': u"orm['truespeak.Facebook_User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plugin_token': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'pubkeys': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['truespeak']