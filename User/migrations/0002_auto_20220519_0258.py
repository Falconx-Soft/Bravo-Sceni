# Generated by Django 3.2.13 on 2022-05-18 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.DeleteModel(
            name='accountsCheck',
        ),
    ]
