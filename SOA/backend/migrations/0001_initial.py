# Generated by Django 4.0.2 on 2024-04-16 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField()),
                ('job_title', models.CharField(max_length=100)),
                ('level', models.TextField()),
                ('corporate', models.TextField()),
                ('requirements', models.TextField()),
            ],
        ),
    ]
