# Generated by Django 2.2.1 on 2019-05-15 19:44

from django.db import migrations

def add_office_foreign_key(apps,schema_editor):
    Office=apps.get_model("nys","Office")
    Filer=apps.get_model("nys","Filer")
    for f in Filer.objects.filter(office_id_lk__isnull=False):
        f.office,__=Office.objects.get_or_create(id=f.office_id_lk)
        f.save()

class Migration(migrations.Migration):

    dependencies = [
        ('nys', '0005_auto_20190515_1916'),
    ]

    operations = [
        migrations.RunPython(add_office_foreign_key,migrations.RunPython.noop),
    ]