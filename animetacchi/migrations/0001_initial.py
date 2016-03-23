# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'News'
        db.create_table(u'animetacchi_news', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('news', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('index_cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('article', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('seq_news', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'animetacchi', ['News'])

        # Adding model 'Members'
        db.create_table(u'animetacchi_members', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('m_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('m_cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('m_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('m_bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('m_tagline', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('seq_members', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'animetacchi', ['Members'])

        # Adding model 'About'
        db.create_table(u'animetacchi_about', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['animetacchi.Members'], null=True, blank=True)),
            ('about', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('seq_about', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'animetacchi', ['About'])

        # Adding model 'Genre'
        db.create_table(u'animetacchi_genre', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('genre_type', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
        ))
        db.send_create_signal(u'animetacchi', ['Genre'])

        # Adding model 'Anime'
        db.create_table(u'animetacchi_anime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('a_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('a_cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('a_displaypic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('a_synopsys', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('a_airedstart', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('a_airedend', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('save_added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('seq_anime', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'animetacchi', ['Anime'])

        # Adding M2M table for field a_genre on 'Anime'
        m2m_table_name = db.shorten_name(u'animetacchi_anime_a_genre')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('anime', models.ForeignKey(orm[u'animetacchi.anime'], null=False)),
            ('genre', models.ForeignKey(orm[u'animetacchi.genre'], null=False))
        ))
        db.create_unique(m2m_table_name, ['anime_id', 'genre_id'])

        # Adding model 'WatchList'
        db.create_table(u'animetacchi_watchlist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('members', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['animetacchi.Members'], null=True, blank=True)),
            ('watchlist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['animetacchi.Anime'], null=True, blank=True)),
            ('seq_watchlist', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'animetacchi', ['WatchList'])


    def backwards(self, orm):
        # Deleting model 'News'
        db.delete_table(u'animetacchi_news')

        # Deleting model 'Members'
        db.delete_table(u'animetacchi_members')

        # Deleting model 'About'
        db.delete_table(u'animetacchi_about')

        # Deleting model 'Genre'
        db.delete_table(u'animetacchi_genre')

        # Deleting model 'Anime'
        db.delete_table(u'animetacchi_anime')

        # Removing M2M table for field a_genre on 'Anime'
        db.delete_table(db.shorten_name(u'animetacchi_anime_a_genre'))

        # Deleting model 'WatchList'
        db.delete_table(u'animetacchi_watchlist')


    models = {
        u'animetacchi.about': {
            'Meta': {'object_name': 'About'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['animetacchi.Members']", 'null': 'True', 'blank': 'True'}),
            'seq_about': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'animetacchi.anime': {
            'Meta': {'object_name': 'Anime'},
            'a_airedend': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'a_airedstart': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'a_cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'a_displaypic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'a_genre': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['animetacchi.Genre']", 'symmetrical': 'False'}),
            'a_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'a_synopsys': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'save_added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'seq_anime': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'animetacchi.genre': {
            'Meta': {'object_name': 'Genre'},
            'genre_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'animetacchi.members': {
            'Meta': {'object_name': 'Members'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'm_bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'm_cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'm_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'm_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'm_tagline': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'seq_members': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'animetacchi.news': {
            'Meta': {'object_name': 'News'},
            'article': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'news': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'seq_news': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'animetacchi.watchlist': {
            'Meta': {'object_name': 'WatchList'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['animetacchi.Members']", 'null': 'True', 'blank': 'True'}),
            'seq_watchlist': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'watchlist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['animetacchi.Anime']", 'null': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['animetacchi']