# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-06-19 01:31
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0014_courseoverview_certificate_available_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course_modes', '0011_change_regex_for_comma_separated_ints'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCourseMode',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('mode_slug', models.CharField(max_length=100, verbose_name='Mode')),
                ('mode_display_name', models.CharField(max_length=255, verbose_name='Display Name')),
                ('min_price', models.IntegerField(default=0, verbose_name='Price')),
                ('currency', models.CharField(default='usd', max_length=8)),
                ('_expiration_datetime', models.DateTimeField(blank=True, db_column='expiration_datetime', default=None, help_text='OPTIONAL: After this date/time, users will no longer be able to enroll in this mode. Leave this blank if users can enroll in this mode until enrollment closes for the course.', null=True, verbose_name='Upgrade Deadline')),
                ('expiration_datetime_is_explicit', models.BooleanField(default=False)),
                ('expiration_date', models.DateField(blank=True, default=None, null=True)),
                ('suggested_prices', models.CharField(blank=True, default='', max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('description', models.TextField(blank=True, null=True)),
                ('sku', models.CharField(blank=True, help_text='OPTIONAL: This is the SKU (stock keeping unit) of this mode in the external ecommerce service.  Leave this blank if the course has not yet been migrated to the ecommerce service.', max_length=255, null=True, verbose_name='SKU')),
                ('bulk_sku', models.CharField(blank=True, default=None, help_text='This is the bulk SKU (stock keeping unit) of this mode in the external ecommerce service.', max_length=255, null=True, verbose_name='Bulk SKU')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('course', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='course_overviews.CourseOverview')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical course mode',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
