# Generated by Django 4.2 on 2023-05-10 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0009_medical'),
    ]

    operations = [
        migrations.DeleteModel(
            name='education',
        ),
        migrations.DeleteModel(
            name='medical',
        ),
    ]
