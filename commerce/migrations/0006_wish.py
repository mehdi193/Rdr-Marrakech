# Generated by Django 3.2.6 on 2021-08-24 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commerce', '0005_auto_20210818_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='wish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idPr', models.ForeignKey(null='True', on_delete=django.db.models.deletion.CASCADE, related_name='idPr', to='commerce.produit')),
                ('idUs', models.ForeignKey(null='True', on_delete=django.db.models.deletion.CASCADE, related_name='idUs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
