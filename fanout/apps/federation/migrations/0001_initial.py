# Generated by Django 3.2.11 on 2022-01-07 01:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import fanout.apps.utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.CharField(default=fanout.apps.utils.models.uuid4_string, max_length=512, primary_key=True, serialize=False)),
                ('url', models.CharField(blank=True, max_length=1024, null=True)),
                ('type', models.CharField(choices=[('Accept', 'Accept'), ('Add', 'Add'), ('Announce', 'Announce'), ('Arrive', 'Arrive'), ('Block', 'Block'), ('Create', 'Create'), ('Delete', 'Delete'), ('Dislike', 'Dislike'), ('Flag', 'Flag'), ('Follow', 'Follow'), ('Ignore', 'Ignore'), ('Invite', 'Invite'), ('Join', 'Join'), ('Leave', 'Leave'), ('Like', 'Like'), ('Listen', 'Listen'), ('Move', 'Move'), ('Offer', 'Offer'), ('Question', 'Question'), ('Reject', 'Reject'), ('Read', 'Read'), ('Remove', 'Remove'), ('TentativeReject', 'Tentative Reject'), ('TentativeAccept', 'Tentative Accept'), ('Travel', 'Travel'), ('Undo', 'Undo'), ('Update', 'Update'), ('View', 'View')], default=('Accept', 'Accept'), max_length=15)),
                ('payload', models.JSONField(blank=True, null=True)),
                ('object_id', models.CharField(blank=True, max_length=256, null=True)),
                ('target_id', models.CharField(blank=True, max_length=256, null=True)),
                ('related_object_id', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.CharField(default=fanout.apps.utils.models.uuid4_string, max_length=512, primary_key=True, serialize=False)),
                ('url', models.CharField(blank=True, max_length=1024, null=True)),
                ('type', models.CharField(choices=[('Person', 'Person'), ('Group', 'Group'), ('Organization', 'Organization or Company'), ('Application', 'Application'), ('Service', 'Service')], default=('Person', 'Person'), max_length=12)),
                ('display_name', models.CharField(blank=True, max_length=512, null=True)),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
                ('public_key', models.TextField(blank=True, max_length=5000, null=True)),
                ('private_key', models.TextField(blank=True, max_length=5000, null=True)),
                ('summary', models.CharField(blank=True, max_length=512, null=True)),
                ('summary_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('manually_approves_followers', models.BooleanField(default=False)),
                ('followers_url', models.CharField(blank=True, max_length=2048, null=True)),
                ('inbox_url', models.CharField(blank=True, max_length=2048, null=True)),
                ('outbox_url', models.CharField(blank=True, max_length=2048, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InboxItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('to', 'to'), ('cc', 'cc')], max_length=10)),
                ('is_read', models.BooleanField(default=False)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inbox_items', to='federation.activity')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inbox_items', to='federation.actor')),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.CharField(default=fanout.apps.utils.models.uuid4_string, max_length=512, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('info', models.JSONField(blank=True, max_length=50000, null=True)),
                ('info_updated', models.DateTimeField(blank=True, null=True)),
                ('service_actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_domains', to='federation.actor')),
            ],
            options={
                'ordering': ('-updated_at', '-created_at'),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='actor',
            name='domain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actors', to='federation.domain'),
        ),
        migrations.AddField(
            model_name='actor',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_actors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='actor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outbox_activities', to='federation.actor'),
        ),
        migrations.AddField(
            model_name='activity',
            name='object_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='objecting_activities', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='activity',
            name='recipients',
            field=models.ManyToManyField(related_name='inbox_activities', through='federation.InboxItem', to='federation.Actor'),
        ),
        migrations.AddField(
            model_name='activity',
            name='related_object_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_objecting_activities', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='activity',
            name='target_content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='targeting_activities', to='contenttypes.contenttype'),
        ),
    ]
