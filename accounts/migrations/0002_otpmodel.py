# Generated by Django 2.2.11 on 2020-07-26 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15)),
                ('otp', models.CharField(max_length=10, unique=True)),
                ('count', models.IntegerField(default=0, help_text='Number of otp sent')),
            ],
        ),
    ]