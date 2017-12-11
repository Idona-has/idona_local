# Generated by Django 2.0 on 2017-12-11 17:50

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('idona', '0004_auto_20171211_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='endpointmatrix',
            name='days',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday'), ('wd', 'Weekdays'), ('we', 'Weekend'), ('all', 'All')], default='all', max_length=37),
        ),
    ]
