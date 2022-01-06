# Generated by Django 3.2.11 on 2022-01-06 20:46

from django.db import migrations, models
import django.db.models.deletion
import fanout.apps.utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('federation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('id', models.CharField(default=fanout.apps.utils.models.uuid4_string, max_length=512, primary_key=True, serialize=False)),
                ('url', models.CharField(blank=True, max_length=1024, null=True)),
                ('content', models.TextField(max_length=50000)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='federation.actor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
