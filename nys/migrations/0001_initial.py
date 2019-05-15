# Generated by Django 2.2.1 on 2019-05-13 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommitteeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Filer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filer_id', models.CharField(max_length=8)),
                ('filer_name', models.TextField()),
                ('filer_type', models.CharField(choices=[('O', 'Committee'), ('A', 'Candidate')], max_length=1)),
                ('filer_status', models.CharField(choices=[('I', 'Inactive'), ('A', 'Active')], max_length=1)),
                ('office', models.IntegerField(null=True)),
                ('district', models.IntegerField(null=True)),
                ('treasurer_first_name', models.TextField(blank=True)),
                ('treasurer_last_name', models.TextField(blank=True)),
                ('address', models.TextField(blank=True)),
                ('city', models.TextField(blank=True)),
                ('state', models.TextField(blank=True)),
                ('zipcode', models.TextField(blank=True)),
                ('committee_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='nys.CommitteeType')),
            ],
        ),
    ]
