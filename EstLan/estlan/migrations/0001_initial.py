# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'estlan_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('addr_country_code', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('addr_city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('addr_street', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('map_link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'estlan', ['Location'])

        # Adding model 'Article'
        db.create_table(u'estlan_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('short_text', self.gf('tinymce.models.HTMLField')()),
            ('content', self.gf('tinymce.models.HTMLField')()),
            ('draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
        ))
        db.send_create_signal(u'estlan', ['Article'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'estlan_location')

        # Deleting model 'Article'
        db.delete_table(u'estlan_article')


    models = {
        u'estlan.article': {
            'Meta': {'object_name': 'Article'},
            'content': ('tinymce.models.HTMLField', [], {}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'short_text': ('tinymce.models.HTMLField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'estlan.location': {
            'Meta': {'object_name': 'Location'},
            'addr_city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'addr_country_code': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'addr_street': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['estlan']