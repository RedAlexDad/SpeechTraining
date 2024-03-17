# Generated by Django 3.2.15 on 2024-03-17 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transcription',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('transcription_text', models.TextField(null=True)),
                ('wer', models.IntegerField(null=True)),
                ('cer', models.IntegerField(null=True)),
                ('mer', models.IntegerField(null=True)),
                ('wil', models.IntegerField(null=True)),
            ],
        ),
    ]