# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.utils.text import slugify

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."

        feature_types = db.execute("select distinct feature_type from content_content")
        for feature_type in feature_types:
            ft = orm.FeatureType.objects.get_or_create(
                name=feature_type,
                slug=slugify(feature_type)
            )
            db.execute("update content_content set feature_type_d = %s where feature_type = '%s'", [ft.id, feature_type])

        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        user_model_label: {
            'Meta': {'object_name': User.__name__, 'db_table': "'%s'" % User._meta.db_table},
            User._meta.pk.attname: ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'%s'" % User._meta.pk.column}),
        },
        u'content.content': {
            'Meta': {'object_name': 'Content'},
            '_thumbnail': ('djbetty.fields.ImageField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['%s']" % user_model_label, 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'feature_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.FeatureType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indexed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_content.content_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'published': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'subhead': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['content.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'content.featuretype': {
            'Meta': {'object_name': 'FeatureType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'content.logentry': {
            'Meta': {'ordering': "('-action_time',)", 'object_name': 'LogEntry'},
            'action_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'change_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'change_logs'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'change_logs'", 'null': 'True', 'to': u"orm['%s']" % user_model_label})
        },
        u'content.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_content.tag_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['content']
    symmetrical = True
