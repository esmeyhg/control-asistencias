# Generated by Django 3.0.8 on 2020-08-23 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0003_auto_20200704_0228'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asistencia',
            options={'ordering': ['-id'], 'verbose_name': 'Asistencia', 'verbose_name_plural': 'Asistencias'},
        ),
        migrations.AlterModelOptions(
            name='facilitador',
            options={'ordering': ['-id'], 'verbose_name': 'Facilitador', 'verbose_name_plural': 'Facilitadores'},
        ),
        migrations.AlterModelOptions(
            name='proveedor',
            options={'ordering': ['-id'], 'verbose_name': 'Proveedor', 'verbose_name_plural': 'Proveedores'},
        ),
    ]