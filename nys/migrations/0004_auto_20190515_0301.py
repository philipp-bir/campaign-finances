# Generated by Django 2.2.1 on 2019-05-15 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nys', '0003_auto_20190514_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.RenameField(
            model_name='filer',
            old_name='office',
            new_name='office_id',
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('subdivision', models.TextField()),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nys.County')),
            ],
        ),
        migrations.CreateModel(
            name='CountyFiler',
            fields=[
                ('filer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='nys.Filer')),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nys.County')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nys.Municipality')),
            ],
            bases=('nys.filer',),
        ),
    ]
