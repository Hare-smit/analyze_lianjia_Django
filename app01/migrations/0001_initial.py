# Generated by Django 4.1 on 2022-09-17 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_user', models.CharField(max_length=32, verbose_name='管理员')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('plce', models.CharField(max_length=64, verbose_name='地区')),
            ],
        ),
    ]
