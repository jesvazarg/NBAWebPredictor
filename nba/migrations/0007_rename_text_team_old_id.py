# Generated by Django 4.1.7 on 2023-06-06 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0006_team_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='text',
            new_name='old_id',
        ),
    ]
