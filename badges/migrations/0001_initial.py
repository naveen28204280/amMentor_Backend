# Generated by Django 5.2 on 2025-04-15 07:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Badges',
            fields=[
                ('badge', models.CharField(primary_key=True, serialize=False)),
                ('icon', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Badges_Members',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField()),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='badges.badges')),
            ],
        ),
    ]
