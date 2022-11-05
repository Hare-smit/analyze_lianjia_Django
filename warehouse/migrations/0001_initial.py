# Generated by Django 4.1 on 2022-09-05 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Housing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=256)),
                ('community', models.CharField(max_length=64)),
                ('position', models.CharField(max_length=32)),
                ('tag', models.TextField()),
                ('re_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('hoursetype', models.CharField(max_length=64)),
                ('hoursesize', models.DecimalField(decimal_places=2, max_digits=5)),
                ('direction', models.CharField(max_length=32)),
                ('fitment', models.CharField(max_length=32)),
                ('plce', models.CharField(max_length=32)),
            ],
        ),
    ]
