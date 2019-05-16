# Generated by Django 2.2.1 on 2019-05-15 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nys', '0004_auto_20190515_0301'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filer',
            old_name='office_id',
            new_name='office_id_lk',
        ),
        migrations.AddField(
            model_name='filer',
            name='office',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='nys.Office'),
        ),
    ]
