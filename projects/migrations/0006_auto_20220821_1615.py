# Generated by Django 3.2.15 on 2022-08-21 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profiles_location_skills'),
        ('projects', '0005_auto_20220819_0904'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='Project',
            new_name='project',
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('owner', 'project')},
        ),
    ]
