# Generated by Django 3.2.6 on 2021-08-25 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0007_auto_20210825_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='notes',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
