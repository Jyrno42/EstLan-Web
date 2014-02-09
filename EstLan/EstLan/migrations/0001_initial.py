# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'EstLan_location', (
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
        db.send_create_signal(u'EstLan', ['Location'])

        # Adding model 'ObjectComment'
        db.create_table(u'EstLan_objectcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['accounts.EstLanUser'])),
            ('comment', self.gf('tinymce.models.HTMLField')()),
            ('for_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('for_object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
        ))
        db.send_create_signal(u'EstLan', ['ObjectComment'])

        # Adding model 'ArticleCategory'
        db.create_table(u'EstLan_articlecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('name_et', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('name_en_gb', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['EstLan.ArticleCategory'])),
        ))
        db.send_create_signal(u'EstLan', ['ArticleCategory'])

        # Adding model 'Article'
        db.create_table(u'EstLan_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title_et', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('title_en_gb', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('short_text', self.gf('ckeditor.fields.RichTextField')()),
            ('short_text_et', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('short_text_en_gb', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('content', self.gf('ckeditor.fields.RichTextField')()),
            ('content_et', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('content_en_gb', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('cover_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['accounts.EstLanUser'])),
            ('draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pinned', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'EstLan', ['Article'])

        # Adding M2M table for field categories on 'Article'
        m2m_table_name = db.shorten_name(u'EstLan_article_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm[u'EstLan.article'], null=False)),
            ('articlecategory', models.ForeignKey(orm[u'EstLan.articlecategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'articlecategory_id'])

        # Adding model 'SiteMenu'
        db.create_table(u'EstLan_sitemenu', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16, blank=True)),
        ))
        db.send_create_signal(u'EstLan', ['SiteMenu'])

        # Adding model 'CustomPage'
        db.create_table(u'EstLan_custompage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title_et', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('title_en_gb', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('content', self.gf('ckeditor.fields.RichTextField')(blank=True)),
            ('content_et', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('content_en_gb', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['accounts.EstLanUser'])),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['EstLan.SiteMenu'])),
            ('draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'EstLan', ['CustomPage'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'EstLan_location')

        # Deleting model 'ObjectComment'
        db.delete_table(u'EstLan_objectcomment')

        # Deleting model 'ArticleCategory'
        db.delete_table(u'EstLan_articlecategory')

        # Deleting model 'Article'
        db.delete_table(u'EstLan_article')

        # Removing M2M table for field categories on 'Article'
        db.delete_table(db.shorten_name(u'EstLan_article_categories'))

        # Deleting model 'SiteMenu'
        db.delete_table(u'EstLan_sitemenu')

        # Deleting model 'CustomPage'
        db.delete_table(u'EstLan_custompage')


    models = {
        u'EstLan.article': {
            'Meta': {'object_name': 'Article'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['accounts.EstLanUser']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['EstLan.ArticleCategory']", 'symmetrical': 'False'}),
            'content': ('ckeditor.fields.RichTextField', [], {}),
            'content_en_gb': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'content_et': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'cover_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pinned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'short_text': ('ckeditor.fields.RichTextField', [], {}),
            'short_text_en_gb': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'short_text_et': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en_gb': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_et': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'EstLan.articlecategory': {
            'Meta': {'object_name': 'ArticleCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name_en_gb': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'name_et': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['EstLan.ArticleCategory']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'})
        },
        u'EstLan.custompage': {
            'Meta': {'object_name': 'CustomPage'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['accounts.EstLanUser']"}),
            'content': ('ckeditor.fields.RichTextField', [], {'blank': 'True'}),
            'content_en_gb': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'content_et': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['EstLan.SiteMenu']"}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en_gb': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_et': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'EstLan.location': {
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
        },
        u'EstLan.objectcomment': {
            'Meta': {'object_name': 'ObjectComment'},
            'comment': ('tinymce.models.HTMLField', [], {}),
            'for_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'for_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['accounts.EstLanUser']"})
        },
        u'EstLan.sitemenu': {
            'Meta': {'object_name': 'SiteMenu'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16', 'blank': 'True'})
        },
        u'accounts.estlanuser': {
            'Meta': {'object_name': 'EstLanUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "u'm'", 'max_length': '1'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'selected_avatar': ('django.db.models.fields.CharField', [], {'default': "u'fb'", 'max_length': '2'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '16', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['EstLan']